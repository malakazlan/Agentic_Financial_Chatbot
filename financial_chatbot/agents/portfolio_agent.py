import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def get_portfolio_summary(tickers, period="1mo"):
    try:
        data = yf.download(tickers, period=period)["Adj Close"]
        if isinstance(data, pd.Series):
            data = data.to_frame()
        
        returns = (data.iloc[-1] - data.iloc[0]) / data.iloc[0] * 100
        summary = "\n".join([f"{ticker}: {ret:.2f}% return" for ticker, ret in returns.items()])
        
        # Plot portfolio
        data_normalized = data / data.iloc[0]
        plot_path = "portfolio_plot.png"
        data_normalized.plot(figsize=(10, 5), title="Portfolio Performance")
        plt.xlabel("Date")
        plt.ylabel("Normalized Price")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()
        
        return summary, plot_path
    except Exception as e:
        return f"Error: {str(e)}", None
