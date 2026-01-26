import yfinance as yf
import pandas as pd
class VWAP:
    def __init__(self,ticker):
        self.ticker_data = ticker
        self.com_pvp_high = 0
        self.comVol_high = 0
        self.VWAP_HIGH = 0
        self.com_pvp_low = 0
        self.comVol_low = 0
        self.VWAP_LOW = 0
        self.HIGH = 0
        self.LOW = 0
        self.HIGH_FOUND = False
        self.LOW_FOUND = False
        self.VWAP_DF = pd.DataFrame
        self.VWAP_ARRAY_HIGH = []
        self.VWAP_ARRAY_LOW = []
        self.vwap_ticker = self.vwap()

    def get_vwap_ticker(self):
        return self.vwap_ticker

    def vwap(self):
        prices = self.ticker_data

        self.HIGH = self.find_high()
        self.LOW = self.find_low()

        for index,row in prices.iterrows():

            if self.HIGH == row["High"]:
                self.HIGH_FOUND = True

            if self.HIGH_FOUND:
                tp = (row["High"]+row["Low"]+row["Close"])/3
                pvp = tp * row["Volume"]
                self.com_pvp_high += pvp
                self.comVol_high+= row["Volume"]
                self.VWAP_HIGH= self.com_pvp_high / self.comVol_high

                self.VWAP_ARRAY_HIGH.append(self.VWAP_HIGH)
            else:
                self.VWAP_ARRAY_HIGH.append(0)

        for index,row in prices.iterrows():

            if self.LOW == row["Low"]:
                self.LOW_FOUND = True

            if self.LOW_FOUND:
                tp = (row["High"]+row["Low"]+row["Close"])/3
                pvp = tp * row["Volume"]
                self.com_pvp_low += pvp
                self.comVol_low+= row["Volume"]
                self.VWAP_LOW= self.com_pvp_low / self.comVol_low
                self.VWAP_ARRAY_LOW.append(self.VWAP_LOW)
            else:
                self.VWAP_ARRAY_LOW.append(0)

        prices.insert(0,"Vwap_high", self.VWAP_ARRAY_HIGH)
        prices.insert(0, "Vwap_low", self.VWAP_ARRAY_LOW)
        return prices




    def find_high(self):

        prices = self.ticker_data

        sorted_by_high = prices.sort_values(by="High")
        high = sorted_by_high.tail(1)
        return high.iloc[0]["High"]

    def find_low(self):

        prices = self.ticker_data
        sorted_by_low = prices.sort_values(by="Low")
        low = sorted_by_low.head(1)
        return low.iloc[0]["Low"]

