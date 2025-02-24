import psycopg2
from psycopg2 import sql
from contextlib import contextmanager

# Database connection details
DB_HOST = "localhost"
DB_NAME = "cosmofoil"
DB_USER = "text_to_sql_user"
DB_PASSWORD = "NecurePss123"

# Context manager for connecting to the database
@contextmanager
def get_db_connection():
    print("Connecting to the database...")
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    try:
        yield conn
    finally:
        conn.close()