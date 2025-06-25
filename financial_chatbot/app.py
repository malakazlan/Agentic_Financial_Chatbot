from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from agents.query_agent import handle_query
from agents.report_parser_agent import summarize_financial_report
from memory.memory_handler import MemoryBuffer
import streamlit as st

app = FastAPI()

# Allow CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session (for demo; use persistent store for production)
session_memory = MemoryBuffer()
report_ask_fn = None

@app.post("/chat")
async def chat(user_input: str = Form(...)):
    context = session_memory.get_context()
    response = handle_query(user_input)
    session_memory.add(user_input, response)
    if isinstance(response, tuple):
        return {"response": response[0], "image": response[1]}
    return {"response": response}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    summary, ask_fn = summarize_financial_report(file_path)
    global report_ask_fn
    report_ask_fn = ask_fn
    return {"summary": summary}

@app.post("/report-query")
async def report_query(query: str = Form(...)):
    global report_ask_fn
    if report_ask_fn is None:
        return JSONResponse(status_code=400, content={"error": "No report uploaded yet."})
    answer = report_ask_fn(query)
    return {"answer": answer}

# --- Sidebar ---
st.sidebar.title("💹 Financial ChatBot")
st.sidebar.markdown(
    """
    **Conversational financial assistant**
    - Ask about stocks, news, filings, and more
    - Upload and analyze financial reports (PDF)
    - Powered by LLMs and real-time data
    
    [View on GitHub](#)
    """
)

# --- Session State Setup ---
if "memory" not in st.session_state:
    st.session_state.memory = MemoryBuffer()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "report_ask_fn" not in st.session_state:
    st.session_state.report_ask_fn = None
if "report_summary" not in st.session_state:
    st.session_state.report_summary = None

st.set_page_config(page_title="Financial ChatBot", page_icon="💹")
st.title("💹 Financial ChatBot (Real-Time)")

# --- Tabs for Chat and Document Analysis ---
tabs = st.tabs(["💬 Chat", "📄 Document Analysis"])

# --- Tab 1: Financial Chat ---
with tabs[0]:
    st.subheader("Chat with the Financial Bot")
    # Display chat history
    for entry in st.session_state.memory.chat_history:
        st.markdown(f"**You:** {entry['user']}")
        st.markdown(f"**Bot:** {entry['bot']}")
        st.markdown("---")

    user_input = st.text_input("Ask a financial question (e.g., TSLA stock price):", key="chat_input")
    if st.button("Send", key="send_chat") and user_input:
        context = st.session_state.memory.get_context()
        with st.spinner("Thinking..."):
            response = handle_query(user_input)
            st.session_state.memory.add(user_input, response)
            st.session_state.chat_history.append({"user": user_input, "bot": response})
            if isinstance(response, tuple):
                st.success(response[0])
                if response[1]:
                    st.image(response[1])
            else:
                st.success(response)
        st.experimental_rerun()

# --- Tab 2: Document Analysis ---
with tabs[1]:
    st.subheader("Analyze a Financial Report (PDF)")
    uploaded_file = st.file_uploader("Upload a financial report (PDF)", type=["pdf"], key="pdf_uploader")
    if uploaded_file is not None:
        file_path = f"temp_{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        with st.spinner("Reading and indexing report..."):
            summary, report_ask_fn = summarize_financial_report(file_path)
            st.session_state.report_summary = summary
            st.session_state.report_ask_fn = report_ask_fn
        st.success(st.session_state.report_summary)

    if st.session_state.report_ask_fn:
        query = st.text_input("Ask something from this report:", key="report_query")
        if st.button("Ask", key="ask_report") and query:
            with st.spinner("Searching report..."):
                answer = st.session_state.report_ask_fn(query)
                st.success(answer)

## app.py (snippet)

