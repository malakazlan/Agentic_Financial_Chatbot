# Financial Chatbot

The Financial Chatbot is an intelligent, modular application designed to assist users with a wide range of financial queries and tasks. Leveraging the power of Large Language Models (LLMs) and real-time data retrieval, this chatbot provides:

- **Conversational financial assistance**: Ask questions about stocks, financial news, company filings, and more in natural language.
- **Agent-based architecture**: Specialized agents handle tasks such as retrieving stock data, parsing financial reports, managing portfolios, and answering general finance questions.
- **Document parsing**: Upload and analyze financial documents (e.g., PDFs of annual reports or filings) to extract key insights and data points.
- **News and filings integration**: Stay updated with the latest financial news and access company filings directly through the chat interface.
- **Session memory**: Maintains chat history and context for more coherent and personalized conversations.
- **Streamlit interface**: User-friendly web interface for seamless interaction.
- **REST API (FastAPI)**: Backend endpoints for integration with custom web frontends (JS/HTML/CSS).

This project is ideal for investors, analysts, students, or anyone seeking quick, reliable financial information and analysis through a conversational interface.

A modular, agent-based financial chatbot built with Streamlit, FastAPI, and LLM integration.

## Project Structure

```
financial_chatbot/
│
├── app.py                      # Streamlit app & FastAPI backend
├── .env                        # Store API keys (use python-dotenv)
│
├── agents/                     # Agent-based logic
│   ├── query_agent.py
│   ├── stock_data_agent.py
│   ├── report_parser_agent.py
│   ├── portfolio_agent.py
│
├── llm/                        # LLM integration
│   ├── chat_engine.py
│   ├── prompt_templates.py
│
├── data/                       # Data loaders and retrievers
│   ├── financial_news.py
│   ├── pdf_loader.py
│   ├── filings_index.py
│
├── utils/                      # Utility functions
│   ├── api_utils.py
│   ├── format_utils.py
│
├── memory/                     # Chat history and session tracking
│   ├── memory_handler.py
│
├── requirements.txt            # Dependencies
└── README.md
```

## Setup

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your API keys.

## Running the Backend

### Streamlit (for reference UI)
```bash
streamlit run app.py
```

### FastAPI (for custom JS/HTML/CSS frontend)
```bash
uvicorn app:app --reload
```
- The API will be available at `http://localhost:8000` by default.
- CORS is enabled for all origins (for development).

#### API Endpoints
- `POST /chat` — Chat with the bot. Form field: `user_input`
- `POST /upload` — Upload a PDF report. Form field: `file` (multipart)
- `POST /report-query` — Ask a question about the uploaded report. Form field: `query`

## Building a Custom Frontend
- Use JavaScript (fetch/axios) to call the above endpoints.
- Example:
  ```js
  // Chat
  fetch('http://localhost:8000/chat', { method: 'POST', body: new FormData(/* ... */) })
  // Upload
  fetch('http://localhost:8000/upload', { method: 'POST', body: new FormData(/* ... */) })
  // Report Q&A
  fetch('http://localhost:8000/report-query', { method: 'POST', body: new FormData(/* ... */) })
  ```
- Build your HTML/CSS/JS UI and connect to these endpoints for a modern web experience.

### Modular Frontend Structure
You can use a modular structure for your frontend:
```
frontend/
  index.html      # Main HTML file
  style.css       # CSS for styling
  app.js          # JavaScript for API calls and UI logic
```
- Place the `frontend` folder at the project root or anywhere you like.
- Open `index.html` in your browser (no server needed for static files).
- Make sure your FastAPI backend is running (`uvicorn app:app --reload`).
- The frontend will communicate with the backend at `http://localhost:8000`. 