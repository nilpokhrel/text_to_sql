import re
from fastapi import HTTPException
import json 
import ast

class QueryValidator:
    @staticmethod
    def is_safe_sql(query: str):
        """Check if the SQL query is safe to execute (prevents SQL injection)"""
        forbidden_patterns = [
            r"(--|#)", r"DROP\s+TABLE", r"DELETE\s+FROM",
            r"INSERT\s+INTO", r"UPDATE\s+\w+\s+SET", r"ALTER\s+TABLE",
            r"EXEC(\s|\()", r"UNION\s+SELECT", r"xp_cmdshell"
        ]
        
        ## Allow semicolon only at the end of a single query
        if ";" in query[:-1]:  
            return False
        
        for pattern in forbidden_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return False # Unsafe query detected
        
        return True 

    @staticmethod
    def validate_sql_query(query: str):
        """Raise an exception if the query is not safe"""
        if not QueryValidator.is_safe_sql(query):
            raise HTTPException(status_code=400, detail="Unsafe SQL query detected.")

    @staticmethod
    def extract_llm_response(response):
        # Case 1: If response is already a Python dictionary, return it directly
        if isinstance(response, dict):
            return response
        
        # Case 2: If response is a string, check if it's a JSON or a Python dict
        if isinstance(response, str):
            # Try extracting JSON from code block if present
            sql_match = re.search(r"```sql\n(.*?)```", response, re.DOTALL)

            if sql_match:
                clean_sql = sql_match.group(1).strip()  # Extract and clean JSON string
            else:
                clean_sql = response.strip()  # Assume the whole response is a JSON/dict string
                
            return clean_sql

        print("Unsupported response type:", type(response))
        return None  # Return None for unsupported types