from data.pdf_loader import load_pdf_text
from data.filings_index import chunk_text, build_vector_index, search_index
from llm.chat_engine import get_llm_response

def summarize_financial_report(file_path):
    text = load_pdf_text(file_path)
    chunks = chunk_text(text)
    index, chunk_store = build_vector_index(chunks)

    def ask_from_report(query):
        relevant_chunks = search_index(query, index, chunk_store)
        context = "\n".join(relevant_chunks)
        return get_llm_response(query, context)

    return "Report indexed. You can now ask questions like:\n- What is net income?\n- Explain the risks discussed in the report.", ask_from_report
