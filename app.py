import streamlit as st
import os
from edgar_fetcher import fetch_latest_10k
from rag_pipeline import process_and_embed_document, generate_swot_analysis
from pdf_generator import generate_pdf
from swot_config import SWOT_CATEGORIES
from database import get_vector_store, get_engine
from sqlalchemy import text

def check_collection_has_documents(collection_name: str) -> bool:
    try:
        engine = get_engine()
        with engine.connect() as conn:
            # Check if table exists first
            table_exists = conn.execute(text(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'langchain_pg_collection');"
            )).scalar()
            if not table_exists:
                return False
            
            # Check if collection has documents
            count = conn.execute(
                text("SELECT count(*) FROM langchain_pg_embedding e JOIN langchain_pg_collection c ON e.collection_id = c.uuid WHERE c.name = :name"),
                {"name": collection_name}
            ).scalar()
            return count > 0
    except Exception as e:
        print("Error checking collection:", e)
        return False

st.set_page_config(page_title="SWOT Analysis RAG", layout="wide")

st.title("Company SWOT Analysis Generator")
st.write("Generate a comprehensive SWOT analysis based on the latest SEC 10-K filings.")

# Initialize session state
if "doc_embedded" not in st.session_state:
    st.session_state.doc_embedded = False
if "collection_name" not in st.session_state:
    st.session_state.collection_name = None
if "current_company" not in st.session_state:
    st.session_state.current_company = ""

company_name = st.text_input("Enter Company Name or Ticker (e.g., Apple, AAPL):")

# Reset state if user changes the company name
if company_name and company_name != st.session_state.current_company:
    st.session_state.current_company = company_name
    st.session_state.doc_embedded = False
    st.session_state.collection_name = None

# Step 1: Fetch and Embed
if company_name and not st.session_state.doc_embedded:
    if st.button("Fetch and Embed Documents"):
        collection_name = company_name.lower().replace(" ", "_")
        
        # Check DB first
        if check_collection_has_documents(collection_name):
            st.success(f"Found existing data for '{company_name}' in the database! Skipping download and embedding.")
            st.session_state.doc_embedded = True
            st.session_state.collection_name = collection_name
            st.rerun()
        else:
            with st.spinner("Fetching SEC 10-K Filing..."):
                try:
                    doc_path = fetch_latest_10k(company_name)
                    if not doc_path:
                        st.error(f"Failed to find or download 10-K for '{company_name}'. Try using the exact ticker symbol.")
                    else:
                        st.success("10-K Filing downloaded successfully.")
                        with st.spinner("Processing and Embedding Document (this may take a minute)..."):
                            process_and_embed_document(doc_path, collection_name=collection_name)
                            st.session_state.doc_embedded = True
                            st.session_state.collection_name = collection_name
                            st.success("Document embedded successfully! You can now select categories below.")
                            st.rerun()
                except Exception as e:
                    st.error(f"An error occurred during fetching/embedding: {e}")

# Step 2: Select Categories and Generate Analysis
if st.session_state.doc_embedded:
    st.success(f"Documents for '{company_name}' are ready for analysis.")
    
    st.subheader("Select Categories for Analysis")
    all_categories = list(SWOT_CATEGORIES.keys())
    selected_categories = st.multiselect("Categories", all_categories, default=all_categories)
    
    if st.button("Generate SWOT Analysis"):
        if not selected_categories:
            st.error("Please select at least one category.")
        else:
            try:
                # Re-instantiate the vectorstore from the DB
                vectorstore = get_vector_store(st.session_state.collection_name)
                
                status_placeholder = st.empty()
                progress_bar = st.progress(0)
                
                def update_status(msg):
                    status_placeholder.info(msg)
                
                def update_progress(val):
                    progress_bar.progress(val)
                    
                with st.spinner("Analyzing and Generating SWOT (using NVIDIA LLM)..."):
                    results = generate_swot_analysis(
                        vectorstore, 
                        selected_categories, 
                        status_callback=update_status,
                        progress_callback=update_progress
                    )
                
                status_placeholder.empty()
                progress_bar.empty()
                st.success("SWOT Analysis generated successfully!")
                
                # Display results
                st.header("SWOT Analysis Results")
                for category, subcategories in results.items():
                    with st.expander(f"{category} Analysis", expanded=True):
                        for subcat_name, summary in subcategories.items():
                            st.subheader(subcat_name)
                            st.write(summary)
                            
                # PDF Generation
                with st.spinner("Generating PDF Report..."):
                    pdf_path = f"{company_name.replace(' ', '_')}_SWOT.pdf"
                    generate_pdf(company_name, results, pdf_path)
                    
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="Download PDF Report",
                            data=f,
                            file_name=pdf_path,
                            mime="application/pdf"
                        )
            except Exception as e:
                st.error(f"An error occurred during generation: {e}")
