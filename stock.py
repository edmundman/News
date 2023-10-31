
import yfinance as yf  # Import yfinance for stock data
import requests

def get_stock_prices(tickers):
    # Split the input tickers into a list
    tickers = tickers.split(',')

    # Create an empty dictionary to store the results
    stock_prices = {}

    # Loop through the tickers and fetch the current price for each
    for ticker in tickers:
        try:
            # Create a Ticker object for the current stock ticker
            stock = yf.Ticker(ticker.strip())

            # Get the current price
            current_price = stock.history(period="1d")["Close"].iloc[-1]

            # Store the current price in the dictionary
            stock_prices[ticker] = current_price
        except Exception as e:
            # Handle any errors (e.g., invalid tickers)
            stock_prices[ticker] = "Error: " + str(e)

    return stock_prices