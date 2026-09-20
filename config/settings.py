import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

EXECUTION_MODE = os.getenv("EXECUTION_MODE", "LOCAL")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:8b")

EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")

DATA_DIR = BASE_DIR / os.getenv("DATA_DIR", "data/uploads")
SAMPLE_DOCS_DIR = BASE_DIR / os.getenv("SAMPLE_DOCS_DIR", "data/sample_documents")
CHROMA_PERSIST_DIR = BASE_DIR / os.getenv("CHROMA_PERSIST_DIR", "chroma_db_store")
SQLITE_DB_PATH = BASE_DIR / os.getenv("SQLITE_DB_PATH", "audit_log.db")

COLLECTION_NAME = os.getenv("COLLECTION_NAME", "docshield_collection")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SAMPLE_DOCS_DIR, exist_ok=True)
os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
