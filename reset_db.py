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

with engine.connect() as conn:
    print("Connected to database. Dropping schema public...")
    conn.execute(text("DROP SCHEMA public CASCADE;"))
    print("Recreating schema public...")
    conn.execute(text("CREATE SCHEMA public;"))
    conn.execute(text("GRANT ALL ON SCHEMA public TO postgres;"))
    conn.execute(text("GRANT ALL ON SCHEMA public TO public;"))
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    conn.commit()
    print("Database reset successfully.")
