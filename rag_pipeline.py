import os
import time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
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
    
    # PHASE 1: Calculating & Batching (Live UI feedback)
    # We use a batch size of 100 for the actual push to DB
    batch_size = 100
    for i in range(0, len(splits), batch_size):
        batch = splits[i:i + batch_size]
        
        # This call handles both embedding and insertion in an optimized batch
        vectorstore.add_documents(batch)
        
        if progress_callback:
            # We report progress AFTER each successful batch push
            progress = min((i + batch_size) / len(splits), 1.0)
            progress_callback(progress)

    print("Embedding complete.")
    return vectorstore

@retry(
    stop=stop_after_attempt(20), 
    wait=wait_exponential(multiplier=2, min=4, max=120), 
    before_sleep=log_retry
)
def process_subcategory_batch(vectorstore, llm, questions: list, summary_instruction: str, status_callback=None, stop_event=None) -> str:
    """
    Retrieves context for all questions in a subcategory, then uses a single LLM call 
    to answer them all (Chain of Thought) and generate the final summary. 
    This maximizes speed without losing any accuracy.
    """
    all_context = set()
    retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 8, 'fetch_k': 30})
    
    # 1. Fast Retrieval Phase
    for q in questions:
        if stop_event and stop_event.is_set():
            return "Stopped by user."
            
        if status_callback:
            status_callback(f"Gathering data for: {q}")
            
        docs = retriever.invoke(q)
        for doc in docs:
            all_context.add(doc.page_content)
            
    context_str = "\n\n".join(list(all_context))
    
    # 2. Generation Phase (Single Call)
    if status_callback:
        status_callback("Analyzing data and writing summary...")
        
    numbered_questions = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
    
    prompt = f"""You are an expert financial analyst. Based on the provided context from a company's SEC 10-K report, please perform the following tasks:

TASK 1: Answer each of the following questions accurately. If the answer is not in the context, state "Information not found."
Questions:
{numbered_questions}

TASK 2: Write a final summary paragraph based on your answers from TASK 1.
Follow this instruction strictly:
{summary_instruction}

Context:
{context_str}

Format your response exactly like this:
ANSWERS:
1. [Answer]
2. [Answer]
...

SUMMARY:
[Your summary paragraph here]
"""
    
    response = llm.invoke(prompt)
    content = response.content
    
    # Parse just the summary to send to the UI
    if "SUMMARY:" in content:
        summary = content.split("SUMMARY:")[-1].strip()
    else:
        summary = content
        
    return summary

def generate_swot_analysis(vectorstore, selected_categories: list, status_callback=None, progress_callback=None, summary_callback=None, stop_event=None):
    """
    Generates the SWOT analysis for the selected categories.
    Returns a dictionary of category -> subcategory -> summary text.
    """
    global current_status_callback
    current_status_callback = status_callback
    
    llm = get_llm()
    results = {}
    
    # Calculate total steps (one per subcategory)
    total_steps = 0
    for cat in selected_categories:
        if cat in SWOT_CATEGORIES:
            total_steps += len(SWOT_CATEGORIES[cat])
    
    processed_steps = 0
    
    for category in selected_categories:
        if category not in SWOT_CATEGORIES:
            continue
            
        results[category] = {}
        subcategories = SWOT_CATEGORIES[category]
        
        for subcat_name, subcat_data in subcategories.items():
            if stop_event and stop_event.is_set():
                print("Stop signal received. Terminating SWOT generation.")
                return results

            msg = f"Processing: {category} -> {subcat_name}"
            print(msg)
            
            questions = subcat_data.get("questions", [])
            summary_instruction = subcat_data.get("summary_instruction", "")
            
            summary = process_subcategory_batch(
                vectorstore, 
                llm, 
                questions, 
                summary_instruction, 
                status_callback=status_callback, 
                stop_event=stop_event
            )
            
            # If stopped during the batch, exit
            if summary == "Stopped by user.":
                return results
                
            results[category][subcat_name] = summary
            
            # Call summary callback if provided
            if summary_callback:
                summary_callback(category, subcat_name, summary)
            
            # Update progress
            processed_steps += 1
            if progress_callback and total_steps > 0:
                progress_callback(processed_steps / total_steps)
                
            time.sleep(2)  # Small delay between major subcategories
            
    return results
