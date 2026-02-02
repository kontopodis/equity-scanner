from fontTools.misc.timeTools import timestampNow
import pandas as pd

class StrategyBuilder:
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
        self.active_trade_path = []
        self.active_trade_path_loss = []
        self.dollar_cost_average = 0
        self.strategy_has_run = False
        self.buy_timestamp = timestampNow()
        self.sell_timestamp = timestampNow()
        self.description = 'You buy when you hit the Monthly Pivot area with a StopLoss on S2 and a Take profit on R2 when the close price is above VWAP_HIGH and above MA200 and MA50'

    def run(self):

        for index,day in self.data.iterrows():

            if day["Low"] < day['Pivot_points'] < day['High'] > day['Vwap_high'] and day['Ma_200'] < day['Ma_50'] < day['Low']:
                if self.active_trade:
                    pass
                else:
                    self.buy_price = day['Pivot_points']
                    self.stop_loss = day['Pivot_points_s2']
                    self.take_profit = day['Pivot_points_r2']
                    self.active_trade = True

            if day["Low"] < self.stop_loss:
                if self.active_trade:
                    self.stop_loss_result += self.buy_price - self.stop_loss
                    self.stop_loss_counter += 1
                    self.active_trade = False
                    self.active_trade_path_loss.pop()
                    self.active_trade_path_loss.append(self.stop_loss)



            if day['High'] > self.take_profit:
                if self.active_trade:
                    self.take_profit_result += self.take_profit - self.buy_price
                    self.take_profit_counter += 1
                    self.active_trade = False

            if self.active_trade:
                self.active_trade_path.append(day['Close']-1)
                self.active_trade_path_loss.append(0)
            else:
                self.active_trade_path.append(0)
                self.active_trade_path_loss.append(0)
        if 'active_trade' in self.data:
            t1 = pd.DataFrame({'active_trade':self.active_trade_path})
            self.data.update(t1)
            t2 = pd.DataFrame({"active_trade_loss":self.active_trade_path_loss})
            self.data.update(t2)
        else:
            self.data.insert(0, "active_trade", self.active_trade_path)
            self.data.insert(0, "active_trade_loss", self.active_trade_path_loss)

        self.strategy_has_run = True

    def check(self):
        last_prices = self.data.tail(1)
        result = False
        if last_prices.iloc[0]["Low"] < last_prices.iloc[0]['Pivot_points'] < last_prices.iloc[0]['High'] and last_prices.iloc[0]['Ma_200'] < last_prices.iloc[0]['Ma_50'] < last_prices.iloc[0]['Low']:
            result = True
        return result