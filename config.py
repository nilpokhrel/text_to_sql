# import os

# # API Keys (Replace with your own)
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-key")
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-gemini-key")

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://text_to_sql_user:your_secure_password@db/text_to_sql_db")



DATABASE_URL = "postgresql://text_to_sql_user:your_secure_password@localhost/text_to_sql_db"
# LLM Model Configuration
LLM_PROVIDER = "gemini"  
LLM_MODEL = "gpt-4o" if LLM_PROVIDER == "openai" else "gemini-2.0-flash"

# GPT_VERSION ='gpt-4o'
# GEMINI_VERSION = "gemini-2.0-flash" # "gemini-pro"

OPENAI_API_KEY = 'sk-'
GEMINI_API_KEY = 'AIza-'
