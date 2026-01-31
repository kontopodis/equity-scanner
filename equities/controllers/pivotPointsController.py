from sqlite3.dbapi2 import Timestamp

import pandas as pd


class PivotPoints:
    def __init__(self, ticker):
        self.ticker = ticker
        self.monthly_data = pd.DataFrame
        self.rolling_stamp = pd.Timestamp
        self.stable_stamp = pd.Timestamp
        self.stable_stamp_boolean = True
        self.stable_counter = -1
        self.rolling_counter = -1
        self.pivot_point = 0
        self.pivot_point_array = []
        self.pivot_r1 = 0
        self.pivot_r1_array  = []
        self.pivot_r2 = 0
        self.pivot_r2_array = []
        self.pivot_s1 = 0
        self.pivot_s1_array = []
        self.pivot_s2 = 0
        self.pivot_s2_array = []
        self.complete_data = self.run()

    def run(self):

        for t in self.ticker.iterrows():
            self.rolling_stamp = t[0]
            self.rolling_counter += 1
            if self.stable_stamp_boolean:
                self.stable_stamp = t[0]
                self.stable_stamp_boolean = False
                self.stable_counter = self.rolling_counter

            if self.rolling_stamp.month != self.stable_stamp.month:
                self.stable_stamp_boolean = True
                self.monthly_data = self.ticker[self.stable_counter:self.rolling_counter]
                close = self.monthly_data.tail(1)
                # Actual Pivot below
                pivot = (self.find_high() + self.find_low() + close.iloc[0]['Close']) / 3
                self.pivot_point = pivot

                r1 = (self.pivot_point*2) - self.find_low()
                self.pivot_r1 = r1

                r2 = self.pivot_point + (self.find_high() - self.find_low())
                self.pivot_r2 = r2

                s1 = (self.pivot_point*2) - self.find_high()
                self.pivot_s1 = s1

                s2 = self.pivot_point - (self.find_high() - self.find_low())
                self.pivot_s2 = s2

            self.pivot_point_array.append(self.pivot_point)
            self.pivot_r1_array.append(self.pivot_r1)
            self.pivot_r2_array.append(self.pivot_r2)
            self.pivot_s1_array.append(self.pivot_s1)
            self.pivot_s2_array.append(self.pivot_s2)

        self.ticker.insert(0, "Pivot_points", self.pivot_point_array)
        self.ticker.insert(0, "Pivot_points_r1", self.pivot_r1_array)
        self.ticker.insert(0, "Pivot_points_r2", self.pivot_r2_array)
        self.ticker.insert(0, "Pivot_points_s1", self.pivot_s1_array)
        self.ticker.insert(0, "Pivot_points_s2", self.pivot_s2_array)

        return self.ticker

    def get_all_data(self):
        return self.complete_data

    def find_high(self):

        prices = self.monthly_data

        sorted_by_high = prices.sort_values(by="High")
        high = sorted_by_high.tail(1)
        return high.iloc[0]["High"]

    def find_low(self):

        prices = self.monthly_data
        sorted_by_low = prices.sort_values(by="Low")
        low = sorted_by_low.head(1)
        return low.iloc[0]["Low"]
