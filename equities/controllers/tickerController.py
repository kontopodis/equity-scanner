import yfinance as yf

class TickerController:
    def __init__(self,ticker):
        self.ticker = ticker
        self.data = yf.Ticker(ticker)

    def get_1month_data(self):
        return self.data.history("1mo")

    def get_1year_data(self):
        return self.data.history("12mo")

    def get_5year_data(self):
        return self.data.history("5y")

    def get_description(self):
        return self.data.info["longBusinessSummary"]
