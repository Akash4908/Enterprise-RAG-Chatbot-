import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import Config
from app.vectorstore import VectorStore


class DocumentIngestion:
    def __init__(self):
        self.vectorstore = VectorStore()

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )

    def load_documents(self):
        documents = []

        for file in os.listdir(Config.DOCUMENT_DIR):
            file_path = os.path.join(Config.DOCUMENT_DIR, file)

            if file.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())

            elif file.endswith(".txt") or file.endswith(".md"):
                loader = TextLoader(file_path)
                documents.extend(loader.load())

        return documents

    def process_and_store(self):
        print("📥 Loading documents...")
        docs = self.load_documents()

        if not docs:
            raise ValueError("No documents found in documents folder")

        print("✂️ Splitting into chunks...")
        chunks = self.text_splitter.split_documents(docs)

        texts = [chunk.page_content for chunk in chunks]

        print("🧠 Creating vector store...")

        # CREATE + SAVE + LOAD (IMPORTANT FIX)
        self.vectorstore.create_store(texts)
        self.vectorstore.save_store()
        self.vectorstore.load_store()

        print("✅ Vector store created and loaded successfully")