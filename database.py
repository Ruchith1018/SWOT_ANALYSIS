import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from langchain_community.vectorstores import PGVector
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from sqlalchemy.pool import NullPool

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

def get_engine():
    return create_engine(DATABASE_URL, poolclass=NullPool)

def get_embeddings():
    api_key = os.environ.get("NVIDIA_API_KEY")
    model = os.environ.get("NVIDIA_EMBED_MODEL", "nvidia/nv-embedqa-e5-v5")
    return NVIDIAEmbeddings(model=model, nvidia_api_key=api_key)

def get_vector_store(collection_name: str = "swot_docs"):
    embeddings = get_embeddings()
    return PGVector(
        connection_string=DATABASE_URL,
        embedding_function=embeddings,
        collection_name=collection_name,
        use_jsonb=True,
        engine_args={"poolclass": NullPool}
    )

def init_db():
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS swot_reports (
                id SERIAL PRIMARY KEY,
                session_id TEXT NOT NULL,
                company_name TEXT NOT NULL,
                pdf_data BYTEA NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        conn.commit()

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
