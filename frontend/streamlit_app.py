import streamlit as st
import requests

# =========================
# CONFIGURATION
# =========================
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Enterprise RAG Assistant",
    page_icon="🏢",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1E88E5; text-align: center; margin-bottom: 0px;}
    .sub-header { font-size: 1rem; color: #616A6B; text-align: center; margin-bottom: 2rem;}
</style>
<div class="main-header">🏢 Enterprise Knowledge Assistant</div>
<div class="sub-header">Ask questions about HR policies, employee handbooks, and company guidelines.</div>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "is_ingested" not in st.session_state:
    st.session_state.is_ingested = False

# =========================
# SIDEBAR CONTROLS
# =========================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6062/6062646.png", width=80)
    st.header("Admin Controls")
    st.write("Sync the vector database with the latest documents.")
    
    if st.button("🔄 Sync Documents", type="primary", use_container_width=True):
        with st.status("Syncing knowledge base...", expanded=True) as status:
            try:
                st.write("Triggering ingestion pipeline...")
                response = requests.post(f"{API_URL}/ingest")
                data = response.json()

                if data.get("status") == "success":
                    status.update(label="Sync Complete!", state="complete", expanded=False)
                    st.session_state.is_ingested = True
                    st.success("Documents successfully ingested into FAISS.")
                else:
                    status.update(label="Sync Failed", state="error")
                    st.error(data.get("message"))
            except requests.exceptions.ConnectionError:
                status.update(label="Connection Error", state="error")
                st.error("Cannot connect to backend. Ensure FastAPI is running on port 8000.")

    st.divider()
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# =========================
# CHAT INTERFACE
# =========================
# Display existing chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input Block
if prompt := st.chat_input("E.g., What is the work from home policy?"):
    
    # 1. Stop if documents aren't loaded
    if not st.session_state.is_ingested:
        st.warning("⚠️ The knowledge base is currently empty. Please click 'Sync Documents' in the sidebar first.")
        st.stop()

    # 2. Add user message to UI and state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Fetch response from backend
    with st.chat_message("assistant"):
        with st.spinner("Searching internal documents..."):
            try:
                response = requests.post(
                    f"{API_URL}/query",
                    json={"query": prompt}
                )
                data = response.json()
                
                if data.get("status") == "success":
                    answer = data.get("answer", "No response generated.")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Error: {data.get('message')}")
                    
            except requests.exceptions.ConnectionError:
                st.error("🚨 Cannot connect to backend. Make sure FastAPI is running on port 8000.")