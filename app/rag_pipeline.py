from langchain_groq import ChatGroq
from app.config import Config
from app.vectorstore import VectorStore
from app.memory import ChatMemory


class RAGPipeline:
    def __init__(self):

        # -------------------------
        # VALIDATE API KEY
        # -------------------------
        if not Config.GROQ_API_KEY:
            raise ValueError("❌ GROQ_API_KEY missing in .env file")

        # -------------------------
        # VECTOR STORE
        # -------------------------
        self.vectorstore = VectorStore()

        # retriever is lazy-loaded
        self.retriever = None

        # -------------------------
        # MEMORY
        # -------------------------
        self.memory = ChatMemory()

        # -------------------------
        # LLM (SAFE INIT)
        # -------------------------
        self.llm = ChatGroq(
            api_key=Config.GROQ_API_KEY,
            model=Config.MODEL_NAME
        )

    # =====================================================
    # RETRIEVER (SAFE + FAILPROOF)
    # =====================================================
    def _ensure_retriever(self):
        """
        Loads FAISS only when available
        prevents NoneType crashes
        """
        if self.retriever is None:
            self.retriever = self.vectorstore.get_retriever()

        if self.retriever is None:
            raise ValueError(
                "❌ Vector DB not initialized. Please run /ingest first."
            )

        return self.retriever

    # =====================================================
    # CONTEXT BUILDER (FIXED FOR LANGCHAIN VERSIONS)
    # =====================================================
    def build_context(self, query: str):

        retriever = self._ensure_retriever()

        # SAFE COMPATIBILITY FIX
        try:
            docs = retriever.invoke(query)
        except Exception:
            docs = retriever.get_relevant_documents(query)

        context = "\n\n".join([doc.page_content for doc in docs])

        return context

    # =====================================================
    # PROMPT ENGINE
    # =====================================================
    def build_prompt(self, query: str, context: str, chat_history: str):

        return f"""
You are an Enterprise Knowledge Assistant.

RULES:
- Use ONLY the provided context
- If answer is not present, say: "Information not available in internal documents"
- Be precise and professional
- Do NOT hallucinate

Chat History:
{chat_history}

Context:
{context}

User Question:
{query}

Answer:
""".strip()

    # =====================================================
    # MAIN RAG FLOW
    # =====================================================
    def generate_response(self, query: str):

        # 1. retrieve context
        context = self.build_context(query)

        # 2. memory
        chat_history = self.memory.get_history()

        # 3. prompt
        prompt = self.build_prompt(query, context, chat_history)

        # 4. LLM CALL (SAFE)
        response = self.llm.invoke(prompt)

        if response is None:
            raise ValueError("❌ LLM returned empty response")

        answer = response.content

        # 5. store memory
        self.memory.add_message(query, answer)

        return {
            "query": query,
            "answer": answer,
            "context_used": context
        }