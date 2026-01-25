import yfinance as yf
from equities.controllers.vwapController import VWAP
from equities.controllers.movingAvgController import MovingAverages
class TickerController:
    def __init__(self,ticker):
        self.ticker = ticker
        self.data = yf.Ticker(ticker)

    def get_1month_data(self):
        return self.data.history("1mo")

    def get_1year_data(self):
        return self.data.history("12mo")

    def get_5year_data(self):
        data_to_return = {}
        temp = self.data.history("5y")
        with_vwap = VWAP(temp)
        data_to_return = with_vwap.get_vwap_ticker()

        ma = MovingAverages(data_to_return)
        data_to_return = ma.get_all_ma()
        return data_to_return

    def get_description(self):
        return self.data.info["longBusinessSummary"]
