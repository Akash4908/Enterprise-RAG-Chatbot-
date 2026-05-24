from fastapi import FastAPI
from pydantic import BaseModel

from app.ingestion import DocumentIngestion
from app.rag_pipeline import RAGPipeline


app = FastAPI(
    title="Enterprise RAG Chatbot",
    version="1.0"
)

ingestor = DocumentIngestion()
rag = RAGPipeline()


class QueryRequest(BaseModel):
    query: str


# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def home():
    return {"message": "RAG API running"}


# =========================
# INGEST ENDPOINT
# =========================
@app.post("/ingest")
def ingest_documents():
    try:
        ingestor.process_and_store()

        # reset retriever cache
        rag.retriever = None

        return {
            "status": "success",
            "message": "Documents ingested successfully"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# =========================
# QUERY ENDPOINT
# =========================
@app.post("/query")
def query_rag(request: QueryRequest):
    try:
        result = rag.generate_response(request.query)

        return {
            "status": "success",
            "answer": result["answer"]
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }