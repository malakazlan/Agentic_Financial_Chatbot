import re
from agents.stock_data_agent import get_stock_price
from agents.portfolio_agent import get_portfolio_summary
from data.financial_news import fetch_news_links, summarize_article
from llm.chat_engine import get_llm_response

def extract_tickers(text):
    return re.findall(r"\b[A-Z]{2,5}\b", text)

def handle_query(user_input: str):
    user_input_lower = user_input.lower()

    if "compare" in user_input_lower or "portfolio" in user_input_lower:
        tickers = extract_tickers(user_input)
        if len(tickers) >= 2:
            return get_portfolio_summary(tickers)
        else:
            return "Please specify 2 or more ticker symbols to compare."

    elif "news" in user_input_lower:
        query = user_input.split("news about")[-1].strip()
        links = fetch_news_links(query)
        if not links:
            return "No recent news found."
        summaries = [summarize_article(link) for link in links]
        return "\n\n".join(summaries)

    elif "price" in user_input_lower or "stock" in user_input_lower:
        tickers = extract_tickers(user_input)
        if tickers:
            return get_stock_price(tickers[0])
        else:
            return "Please mention a valid stock ticker (e.g., TSLA, AAPL)."

    elif any(kw in user_input_lower for kw in ["net income", "revenue", "balance sheet", "cash flow", "risks", "summarize report"]):
        return "Please upload a financial report below. Once uploaded, you can ask questions about it."

    else:
        return get_llm_response(user_input)
