# config.py
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DB_URL = os.getenv("DATABASE_URL")  # Optional
