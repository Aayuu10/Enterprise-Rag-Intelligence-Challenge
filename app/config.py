import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    CHROMA_DIR = os.getenv("CHROMA_DIR", "./indexes/chroma")
    SQLITE_PATH = os.getenv("SQLITE_PATH", "./indexes/app.db")
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")

settings = Settings()