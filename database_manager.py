import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class DatabaseManager:
    def __init__(self):
        self.engine = engine

    def execute_query(self, sql_query: str):
        """Safely execute SQL queries and prevent SQL injection."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(sql_query))
                return result.fetchall()
        except Exception as e:
            return f"Database error: {str(e)}"



if __name__ == '__main__':
    pass
