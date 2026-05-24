from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import Config
import os


class VectorStore:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=Config.EMBEDDING_MODEL
        )
        self.db_path = Config.VECTOR_DB_PATH
        self.vectorstore = None

    # -------------------------
    # CREATE VECTOR STORE
    # -------------------------
    def create_store(self, texts):
        if not texts:
            raise ValueError("No documents provided for indexing.")

        self.vectorstore = FAISS.from_texts(
            texts=texts,
            embedding=self.embeddings
        )

        self.save_store()
        return self.vectorstore

    # -------------------------
    # SAVE STORE
    # -------------------------
    def save_store(self):
        if self.vectorstore:
            self.vectorstore.save_local(self.db_path)

    # -------------------------
    # LOAD STORE
    # -------------------------
    def load_store(self):
        """Always load FAISS safely"""
        if os.path.exists(self.db_path):
            self.vectorstore = FAISS.load_local(
                self.db_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            return self.vectorstore

        return None

    # -------------------------
    # GET RETRIEVER
    # -------------------------
    def get_retriever(self):
        """
        Ensure vectorstore is loaded before retrieval
        """
        if self.vectorstore is None:
            self.load_store()

        if self.vectorstore is None:
            raise ValueError(
                "❌ Vector DB not found. Run /ingest first to create embeddings."
            )

        return self.vectorstore.as_retriever(
            search_kwargs={"k": Config.TOP_K}
        )