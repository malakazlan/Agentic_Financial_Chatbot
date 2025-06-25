import urllib.parse
import feedparser
from newspaper import Article

def fetch_news_links(query: str, limit=3):
    encoded_query = urllib.parse.quote_plus(query)  # Fix: encode query
    url = f"https://news.google.com/rss/search?q={encoded_query}+stock+when:7d&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)
    return [entry.link for entry in feed.entries[:limit]]

from llm.chat_engine import get_llm_response

def summarize_article(url: str) -> str:
    try:
        article = Article(url)
        article.download()
        article.parse()
        content = article.text[:1000]  # Limit to avoid overload

        summary = get_llm_response(f"Summarize this news article:\n{content}")
        return f"🔗 {url}\n📰 {summary}"
    except Exception as e:
        return f"🔗 {url}\n⚠️ Could not summarize: {str(e)}"
