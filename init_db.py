import os
import psycopg2
from urllib.parse import urlparse

def get_db_connection():
    # Use environment variables for connection details
    db_url = os.environ.get("DATABASE_URL", "postgresql://user:password@localhost:5432/mydb")
    return psycopg2.connect(db_url)

def initialize_database():
    conn = get_db_connection()
    cur = conn.cursor()

    # Create users table (idempotent)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # --- Add tables for Agentic Workflow ---

    # 1. Enable pgvector extension
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    
    # 2. Create projects table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name VARCHAR(255) NOT NULL,
            owner_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 3. Create a table to store generated artifacts and their embeddings
    cur.execute("""
        CREATE TABLE IF NOT EXISTS artifacts (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            thread_id UUID NOT NULL,
            agent_name VARCHAR(255) NOT NULL,
            artifact_type VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            embedding vector(1536), -- Adjust size based on your embedding model
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS artifacts_thread_id_idx ON artifacts (thread_id);")

    # 4. Create tables for LangGraph checkpointing
    # These tables are based on the schema required by `langgraph.checkpoint.aiopostgres.PostgresSaver`
    cur.execute("""
         CREATE TABLE IF NOT EXISTS langgraph_threads (
            thread_id UUID PRIMARY KEY,
            project_id UUID REFERENCES projects(id) ON DELETE CASCADE, -- Link to project
            thread_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            tags TEXT[],
            metadata JSONB
         );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS langgraph_checkpoints (
            thread_id UUID NOT NULL,
            checkpoint_ns VARCHAR(64) NOT NULL,
            checkpoint_id UUID NOT NULL,
            parent_checkpoint_id UUID,
            task_id UUID,
            task_ns VARCHAR(64),
            checkpoint JSONB,
            metadata JSONB,
            PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id)
        );
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS langgraph_checkpoints_thread_id_checkpoint_ns_ts_idx
        ON langgraph_checkpoints (thread_id, checkpoint_ns, checkpoint_id DESC);
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS langgraph_checkpoints_task_id_task_ns_idx
        ON langgraph_checkpoints (task_id, task_ns);
    """)


    conn.commit()
    cur.close()
    conn.close()
    print("Database initialized successfully with agentic workflow tables.")

if __name__ == "__main__":
    # Ensure environment variables are loaded if you use a .env file
    from dotenv import load_dotenv
    load_dotenv()
    initialize_database()


