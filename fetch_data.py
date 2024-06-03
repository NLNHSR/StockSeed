import yfinance as yf

def fetch_stock_data(symbol, period='1y'):
    stock = yf.Ticker(symbol)
    hist = stock.history(period=period)
    return hist['Close'].values
