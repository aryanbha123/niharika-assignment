import psycopg2
from psycopg2.extras import RealDictCursor
import time
import os

DATABASE_URL = "postgresql://user:password@localhost/mydb"

def get_db_connection():
    conn = None
    while conn is None:
        try:
            conn = psycopg2.connect(
                DATABASE_URL,
                cursor_factory=RealDictCursor
            )
        except psycopg2.OperationalError as e:
            print(f"Database connection error: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)
    return conn
