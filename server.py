from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from sqlalchemy import text
import asyncio
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

@app.on_event("startup")
async def startup_event():
    # Ensure database tables exist
    init_db()

@app.get("/categories")
async def get_categories():
    return list(SWOT_CATEGORIES.keys())

@app.post("/fetch_and_embed")
async def fetch_and_embed(req: FetchRequest):
    collection_name = req.company_name.lower().replace(" ", "_")
    
    # Check DB first
    if check_collection_has_documents(collection_name):
        return {"status": "success", "collection_name": collection_name, "cached": True}
        
    try:
        doc_path = fetch_latest_10k(req.company_name)
        if not doc_path:
            return {"status": "error", "message": "Filing not found"}
            
        process_and_embed_document(doc_path, collection_name=collection_name)
        return {"status": "success", "collection_name": collection_name}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.delete("/cleanup/{session_id}")
async def cleanup_session(session_id: str):
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM swot_reports WHERE session_id = :session_id"), {"session_id": session_id})
        conn.commit()
    return {"status": "success"}

@app.post("/generate_swot")
async def generate_swot_stream(req: GenerateRequest):
    async def event_generator():
        queue = asyncio.Queue()
        collection_name = req.company_name.lower().replace(" ", "_")
        vectorstore = get_vector_store(collection_name)
        
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
                    summary_callback=summary_callback
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
