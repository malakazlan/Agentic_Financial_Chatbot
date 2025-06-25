import yfinance as yf

def get_stock_price(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        if hist.empty:
            return f"No data found for {ticker}."

        current_price = hist["Close"].iloc[-1]
        return f"{ticker.upper()} is trading at ${current_price:.2f}."
    except Exception as e:
        return f"Error retrieving stock data: {str(e)}"
