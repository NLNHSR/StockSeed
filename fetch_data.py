import yfinance as yf

def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1y")
    return hist['Close'].values
