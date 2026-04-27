import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

database_url = os.environ.get("DATABASE_URL")
if not database_url:
    print("DATABASE_URL not found in .env")
    exit(1)

# Fix connection string for psycopg2 compatibility (if starts with postgres://)
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(database_url)

def truncate_tables():
    with engine.connect() as conn:
        print("Connected to database. Cleaning data but preserving schema...")
        
        # Tables to truncate
        tables = [
            "langchain_pg_embedding",
            "langchain_pg_collection",
            "swot_reports"
        ]
        
        for table in tables:
            try:
                print(f"Truncating {table}...")
                conn.execute(text(f"TRUNCATE TABLE {table} CASCADE;"))
                conn.commit()
            except Exception as e:
                print(f"Skipping {table}: {e}")
                
        print("\nDatabase reset complete. All records deleted, tables preserved.")

if __name__ == "__main__":
    truncate_tables()
