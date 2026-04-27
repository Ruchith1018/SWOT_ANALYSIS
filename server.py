from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from sqlalchemy import text
import asyncio
import threading
import json
import os

from edgar_fetcher import fetch_latest_10k
from rag_pipeline import process_and_embed_document, generate_swot_analysis
from pdf_generator import generate_pdf
from swot_config import SWOT_CATEGORIES
from database import get_vector_store, get_engine, init_db, check_collection_has_documents

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class FetchRequest(BaseModel):
    company_name: str

class GenerateRequest(BaseModel):
    company_name: str
    categories: List[str]
    session_id: str

# Track stop signals for each session
stop_signals = {}

@app.on_event("startup")
async def startup_event():
    # Ensure database tables exist
    init_db()

@app.get("/categories")
async def get_categories():
    return list(SWOT_CATEGORIES.keys())

@app.post("/fetch_and_embed")
async def fetch_and_embed_stream(req: FetchRequest):
    async def event_generator():
        queue = asyncio.Queue()
        loop = asyncio.get_event_loop()
        collection_name = req.company_name.lower().replace(" ", "_")
        
        # Check DB first
        if check_collection_has_documents(collection_name):
            yield f"data: {json.dumps({'type': 'complete', 'collection_name': collection_name, 'cached': True})}\n\n"
            return

        def run_task():
            try:
                # 1. Fetch Progress (Start)
                asyncio.run_coroutine_threadsafe(queue.put({"type": "fetch_progress", "val": 0.5}), loop)
                doc_path = fetch_latest_10k(req.company_name)
                
                if not doc_path:
                    asyncio.run_coroutine_threadsafe(queue.put({"type": "error", "msg": "Filing not found"}), loop)
                    return
                
                asyncio.run_coroutine_threadsafe(queue.put({"type": "fetch_progress", "val": 1.0}), loop)
                
                # 2. Embed Progress
                def embed_cb(p):
                    asyncio.run_coroutine_threadsafe(queue.put({"type": "embed_progress", "val": p}), loop)
                
                process_and_embed_document(doc_path, collection_name=collection_name, progress_callback=embed_cb)
                
                asyncio.run_coroutine_threadsafe(queue.put({"type": "complete", "collection_name": collection_name}), loop)
            except Exception as e:
                asyncio.run_coroutine_threadsafe(queue.put({"type": "error", "msg": str(e)}), loop)
            finally:
                asyncio.run_coroutine_threadsafe(queue.put(None), loop)

        threading.Thread(target=run_task).start()

        while True:
            item = await queue.get()
            if item is None:
                break
            yield f"data: {json.dumps(item)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.delete("/cleanup/{session_id}")
async def cleanup_session(session_id: str):
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM swot_reports WHERE session_id = :session_id"), {"session_id": session_id})
        conn.commit()
    return {"status": "success"}

@app.post("/stop/{session_id}")
async def stop_generation(session_id: str):
    if session_id in stop_signals:
        stop_signals[session_id].set()
        return {"status": "success", "message": "Stop signal sent"}
    return {"status": "error", "message": "No active generation for this session"}

@app.post("/generate_swot")
async def generate_swot_stream(req: GenerateRequest, request: Request):
    async def event_generator():
        queue = asyncio.Queue()
        collection_name = req.company_name.lower().replace(" ", "_")
        vectorstore = get_vector_store(collection_name)
        
        # Create stop signal for this session
        stop_event = threading.Event()
        stop_signals[req.session_id] = stop_event
        
        def status_callback(msg):
            asyncio.run_coroutine_threadsafe(queue.put({"type": "status", "msg": msg}), loop)
            
        def progress_callback(val):
            asyncio.run_coroutine_threadsafe(queue.put({"type": "progress", "val": val}), loop)

        def summary_callback(cat, subcat, content):
            asyncio.run_coroutine_threadsafe(queue.put({
                "type": "summary", 
                "category": cat, 
                "subcat": subcat, 
                "content": content
            }), loop)

        loop = asyncio.get_event_loop()
        
        async def run_generation():
            try:
                results = await asyncio.to_thread(
                    generate_swot_analysis, 
                    vectorstore, 
                    req.categories, 
                    status_callback=status_callback,
                    progress_callback=progress_callback,
                    summary_callback=summary_callback,
                    stop_event=stop_event
                )
                
                # Generate PDF as bytes
                pdf_bytes = await asyncio.to_thread(generate_pdf, req.company_name, results)
                
                # Save to database
                engine = get_engine()
                with engine.connect() as conn:
                    # Clear any existing reports for this session/company to avoid bloat
                    conn.execute(text("DELETE FROM swot_reports WHERE session_id = :sid AND company_name = :cname"), 
                                {"sid": req.session_id, "cname": req.company_name})
                    
                    # Insert new report
                    result = conn.execute(text("""
                        INSERT INTO swot_reports (session_id, company_name, pdf_data)
                        VALUES (:sid, :cname, :data)
                        RETURNING id
                    """), {"sid": req.session_id, "cname": req.company_name, "data": pdf_bytes})
                    report_id = result.fetchone()[0]
                    conn.commit()
                
                await queue.put({"type": "complete", "results": results, "report_id": report_id})
            except Exception as e:
                await queue.put({"type": "error", "msg": str(e)})
            finally:
                if req.session_id in stop_signals:
                    del stop_signals[req.session_id]
                await queue.put(None)

        asyncio.create_task(run_generation())

        while True:
            data = await queue.get()
            if data is None:
                break
            yield f"data: {json.dumps(data)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/download/{report_id}")
async def download_report(report_id: int):
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT company_name, pdf_data FROM swot_reports WHERE id = :id"), {"id": report_id})
        row = result.fetchone()
        if row:
            company_name, pdf_data = row
            filename = f"{company_name.replace(' ', '_')}_SWOT.pdf"
            return Response(
                content=bytes(pdf_data), 
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
    return {"error": "Report not found"}

# Mount the frontend
if not os.path.exists("frontend"):
    os.makedirs("frontend")
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
