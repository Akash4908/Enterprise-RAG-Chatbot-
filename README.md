

# 🧠 Enterprise Knowledge Chatbot (RAG System)

A production-style **Retrieval-Augmented Generation (RAG)** chatbot built using:

- FastAPI (Backend)
- Streamlit (Frontend)
- FAISS (Vector Database)
- HuggingFace Embeddings
- Groq LLM (Llama 3)
- LangChain

---

## 🚀 Features

- Upload and ingest documents (PDF, TXT, MD)
- Semantic search using FAISS vector DB
- Context-aware AI responses (RAG pipeline)
- Chat memory support (multi-turn conversation)
- Fast API backend with Streamlit UI

---

## 🛠️ Project Setup Guide

---

# 1️⃣ Clone the Repository

```bash
git clone https://github.com/Akash4908/Enterprise-RAG-Chatbot-.git
cd enterprise_rag_chatbot
```

---

# 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows
```bash
venv\Scripts\activate
```

### macOS / Linux
```bash
source venv/bin/activate
```

---

# 3️⃣ Install Required Libraries

```bash
python -m pip install --upgrade pip
```

### Option A: Install using requirements.txt (Recommended)

```bash
pip install -r requirements.txt
```

### Option B: Install individually

```bash
pip install fastapi uvicorn
pip install langchain langchain-community langchain-core
pip install faiss-cpu
pip install sentence-transformers
pip install python-dotenv
pip install pypdf
pip install streamlit requests
pip install langchain-groq
```

---

# 4️⃣ Create `.env` File

Copy `.env.example` to `.env` and add your Groq API key:

```bash
cp .env.example .env
```

Edit `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.1-8b-instant
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

---

# 5️⃣ Get API Key (Groq)

1. Go to:
   👉 [https://console.groq.com/](https://console.groq.com/)

2. Sign up / Login

3. Go to:

   * API Keys → Create Key

4. Copy and paste into `.env`

---

# 6️⃣ Project Structure

```
enterprise_rag_chatbot/
│
├── app/
│   ├── main.py              # FastAPI backend
│   ├── ingestion.py         # Document ingestion logic
│   ├── rag_pipeline.py      # RAG query pipeline
│   ├── vectorstore.py       # FAISS vector DB
│   ├── memory.py            # Chat memory management
│   ├── config.py            # Configuration
│   └── auth.py              # Authentication (if needed)
│
├── frontend/
│   └── streamlit_app.py     # Streamlit UI
│
├── documents/               # Upload your PDFs/TXT here
├── vectorstore/             # Auto-generated FAISS DB
├── .env                     # ⚠️ Never commit this!
├── .env.example             # Template for .env
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
└── README.md
```

---

# 7️⃣ Run Backend (FastAPI)

```bash
uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

# 8️⃣ Run Frontend (Streamlit)

In a new terminal (with venv activated):

```bash
streamlit run frontend/streamlit_app.py
```

Your app will be available at: `http://localhost:8501`

---

# 9️⃣ API Endpoints (Backend)

Once FastAPI is running, visit: `http://127.0.0.1:8000/docs`

### Available Endpoints

- **GET `/`** - Health check
- **POST `/ingest`** - Ingest documents (multipart/form-data)
- **POST `/query`** - Query the RAG pipeline
  ```json
  {
    "query": "What are company policies?"
  }
  ```

---

# 🔟 How to Use the System

### Step 1 — Ingest Documents

1. Open Streamlit app
2. Click **📥 Load Documents (Ingest)**
3. Upload PDF/TXT files from `documents/` folder
4. Wait for ingestion to complete

### Step 2 — Ask Questions

In Streamlit UI, type questions like:

```
What are the company values?
What are office hours?
Summarize the leave policy
Can you explain the onboarding process?
```

The chatbot will retrieve relevant documents and answer using the Llama 3 model.

---

## 📚 Example Questions

- "What does the onboarding guide say?"
- "Summarize the leave policy in 3 points"
- "What are employee benefits?"
- "Can you explain the HR policies?"

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **GROQ_API_KEY not found** | Make sure `.env` file exists with valid key |
| **Streamlit won't connect to backend** | Check if FastAPI is running on `http://127.0.0.1:8000` |
| **FAISS index errors** | Delete `vectorstore/` folder and re-ingest documents |
| **Port 8000 already in use** | Run with different port: `uvicorn app.main:app --reload --port 8001` |
| **Module not found errors** | Ensure virtual environment is activated and all packages installed |

---

## 📝 Notes

- Documents are stored in the `documents/` folder
- FAISS vector database is auto-generated in `vectorstore/`
- Chat history is maintained during the session
- Keep `.env` file secret (added to `.gitignore`)

---

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

---

## 📄 License

MIT License - Feel free to use for educational and commercial purposes.
