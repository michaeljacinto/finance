import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from yahoo_fin import stock_info as si

def get_highest_performing_stocks(tickers, period):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=period)

    all_returns = {}
    chunk_size = 50  # Process in chunks to avoid API rate limits
    for i in range(0, len(tickers), chunk_size):
        tickers_chunk = tickers[i:i + chunk_size]
        try:
            stock_data = yf.download(tickers_chunk, start=start_date, end=end_date)
            if 'Adj Close' in stock_data:
                stock_data = stock_data['Adj Close']
                returns = stock_data.pct_change().iloc[1:]
                cumulative_returns = (1 + returns).prod() - 1
                if isinstance(cumulative_returns, pd.Series):
                    all_returns.update(cumulative_returns.to_dict())
                else:
                    all_returns[tickers_chunk[0]] = cumulative_returns
        except Exception as e:
            print(f"Error downloading data for tickers {tickers_chunk}: {e}")
    
    sorted_stocks = pd.Series(all_returns).sort_values(ascending=False)
    return sorted_stocks

# Get a comprehensive list of stock tickers from yahoo_fin
tickers = si.tickers_sp500()  # Example: S&P 500 tickers. You can also use other lists or combine multiple lists
tickers = si.tickers_nasdaq()  # For NASDAQ
# tickers = si.tickers_dow()  # For Dow Jones
tickers.extend(si.tickers_other())  # For other tickers

periods = {
    '1 Month': 30,
    '3 Months': 90,
    '6 Months': 180
}

for period_name, period_days in periods.items():
    top_stocks = get_highest_performing_stocks(tickers, period_days)
    print(f"\nTop performing stocks for the last {period_name}:")
    print(top_stocks.head(10))  # Display the top 10 stocks for brevity
