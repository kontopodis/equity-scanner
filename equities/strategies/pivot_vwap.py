from fontTools.misc.timeTools import timestampNow


class BuyOnPivotAboveVwap:
    def __init__(self,data):
        self.data = data
        self.buy_price = 0
        self.stop_loss = 0
        self.take_profit = 0
        self.stop_loss_result = 0
        self.take_profit_result = 0
        self.stop_loss_counter = 0
        self.take_profit_counter = 0
        self.active_trade = False
        self.dollar_cost_average = 0
        self.buy_timestamp = timestampNow()
        self.sell_timestamp = timestampNow()
        self.run()

    def run(self):

        for index,day in self.data.iterrows():

            if day["Low"] < day['Pivot_points'] < day['High'] > day['Vwap_high']:
                if self.active_trade:
                    pass
                else:
                    self.buy_price = day['Pivot_points']
                    self.stop_loss = day['Pivot_points_s2']
                    self.take_profit = day['Pivot_points_r2']
                    print("Bought at: ", self.buy_price)
                    self.active_trade = True

            if day["Low"] < self.stop_loss:
                if self.active_trade:
                    self.stop_loss_result += self.buy_price - self.stop_loss
                    self.stop_loss_counter += 1
                    self.active_trade = False
                    print("Stopped at: ", self.stop_loss)


            if day['High'] > self.take_profit:
                if self.active_trade:
                    self.take_profit_result += self.take_profit - self.buy_price
                    self.take_profit_counter += 1
                    self.active_trade = False
                    print("Took Profit at: ", self.take_profit)
