import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # LLM Model
    MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")

    # Embedding Model
    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DOCUMENT_DIR = os.path.join(BASE_DIR, "documents")
    VECTOR_DB_PATH = os.path.join(BASE_DIR, "vectorstore")

    # RAG Settings
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 150
    TOP_K = 4