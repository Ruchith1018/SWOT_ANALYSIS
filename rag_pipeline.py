import os
import time
from tenacity import retry, stop_after_attempt, wait_exponential
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from database import get_vector_store
from swot_config import SWOT_CATEGORIES

current_status_callback = None

def log_retry(retry_state):
    msg = f"⚠️ Rate limit hit! Pausing for {retry_state.next_action.sleep:.1f} seconds before retrying..."
    print(msg)
    if current_status_callback:
        current_status_callback(msg)

def get_llm():
    api_key = os.environ.get("NVIDIA_API_KEY")
    model = os.environ.get("NVIDIA_LLM_MODEL", "meta/llama-3.3-70b-instruct")
    return ChatNVIDIA(model=model, nvidia_api_key=api_key)

def process_and_embed_document(file_path: str, collection_name: str = "swot_docs", progress_callback=None):
    print(f"Loading document: {file_path}")
    loader = TextLoader(file_path, encoding='utf-8')
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    splits = text_splitter.split_documents(docs)
    
    # Store source info
    for split in splits:
        split.metadata["source"] = collection_name
        
    print(f"Embedding {len(splits)} chunks into PostgreSQL...")
    vectorstore = get_vector_store(collection_name)
    
    # Embed in batches to show progress
    batch_size = 10
    for i in range(0, len(splits), batch_size):
        batch = splits[i:i + batch_size]
        vectorstore.add_documents(batch)
        if progress_callback:
            progress = min((i + batch_size) / len(splits), 1.0)
            progress_callback(progress)

    print("Embedding complete.")
    return vectorstore

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=2, min=4, max=60), before_sleep=log_retry)
def answer_question(vectorstore, llm, question: str) -> str:
    # Retrieve relevant chunks using MMR for diversity
    retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 15, 'fetch_k': 50})
    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])
    
    prompt = f"""You are a financial analyst. Based on the following excerpts from a company's SEC 10-K report, answer the question accurately. 
If the answer is not in the context, state that you cannot find the information.

Context:
{context}

Question:
{question}

Answer:"""
    
    response = llm.invoke(prompt)
    return response.content

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=2, min=4, max=60), before_sleep=log_retry)
def summarize_subcategory(llm, subcategory_name: str, questions_and_answers: list, summary_instruction: str) -> str:
    qa_text = ""
    for q, a in questions_and_answers:
        qa_text += f"Q: {q}\nA: {a}\n\n"
        
    prompt = f"""You are an expert financial analyst writing a section of a SWOT report.
Follow this instruction strictly:
{summary_instruction}

Here are the questions and the gathered answers based on the company's 10-K:
{qa_text}

Summary Paragraph:"""

    response = llm.invoke(prompt)
    return response.content

def generate_swot_analysis(vectorstore, selected_categories: list, status_callback=None, progress_callback=None, summary_callback=None, stop_event=None):
    """
    Generates the SWOT analysis for the selected categories.
    Returns a dictionary of category -> subcategory -> summary text.
    """
    global current_status_callback
    current_status_callback = status_callback
    
    llm = get_llm()
    results = {}
    
    # Calculate total steps (questions + summaries) for granular progress tracking
    total_steps = 0
    for cat in selected_categories:
        if cat in SWOT_CATEGORIES:
            for subcat_name, subcat_data in SWOT_CATEGORIES[cat].items():
                total_steps += len(subcat_data["questions"]) # One step per question
                total_steps += 1 # One step for the summary
    
    processed_steps = 0
    
    for category in selected_categories:
        if category not in SWOT_CATEGORIES:
            continue
            
        results[category] = {}
        subcategories = SWOT_CATEGORIES[category]
        
        for subcat_name, subcat_data in subcategories.items():
            msg = f"Processing: {category} -> {subcat_name}"
            print(msg)
            if status_callback:
                status_callback(msg)
                
            qna_list = []
            for question in subcat_data["questions"]:
                # Check for stop signal at question level
                if stop_event and stop_event.is_set():
                    print("Stop signal received. Terminating SWOT generation.")
                    return results
                
                msg = f"Answering: {question}"
                print(msg)
                if status_callback:
                    status_callback(msg)
                    
                answer = answer_question(vectorstore, llm, question)
                qna_list.append((question, answer))
                
                # Update progress for each question
                processed_steps += 1
                if progress_callback and total_steps > 0:
                    progress_callback(processed_steps / total_steps)
                
                time.sleep(2)  # Delay to respect rate limits
            
            summary_msg = f"Summarizing: {subcat_name}"
            print(summary_msg)
            if status_callback:
                status_callback(summary_msg)
                
            summary = summarize_subcategory(llm, subcat_name, qna_list, subcat_data["summary_instruction"])
            results[category][subcat_name] = summary
            
            # Call summary callback if provided
            if summary_callback:
                summary_callback(category, subcat_name, summary)
            
            # Update progress for each summary
            processed_steps += 1
            if progress_callback and total_steps > 0:
                progress_callback(processed_steps / total_steps)
                
            time.sleep(3)  # Delay between subcategories
            
    return results
