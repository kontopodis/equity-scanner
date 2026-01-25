class MovingAverages:
    def __init__(self, ticker):
        self.ticker_data = ticker
        self.ma21 = []
        self.ma21_rows = []
        self.complete_data = []
        self.ma50 = []
        self.ma50_rows = []
        self.ma100 = []
        self.ma100_rows = []
        self.ma200 = []
        self.ma200_rows = []
        self.run()

    def run(self):
        data = self.ticker_data
        for index, row in data.iterrows():

            self.ma21.append(row["Close"])
            if len(self.ma21) >= 21:
                self.ma21_rows.append(self.moving_average_21())
                self.ma21.pop(0)
            else:
                self.ma21_rows.append(0)

            self.ma50.append(row["Close"])
            if len(self.ma50) >= 50:
                self.ma50_rows.append(self.moving_average_50())
                self.ma50.pop(0)
            else:
                self.ma50_rows.append(0)

            self.ma100.append(row["Close"])
            if len(self.ma100) >= 100:
                self.ma100_rows.append(self.moving_average_100())
                self.ma100.pop(0)
            else:
                self.ma100_rows.append(0)

            self.ma200.append(row["Close"])
            if len(self.ma200) >= 200:
                self.ma200_rows.append(self.moving_average_200())
                self.ma200.pop(0)
            else:
                self.ma200_rows.append(0)



        data.insert(0, "Ma_21", self.ma21_rows)
        data.insert(0, "Ma_50", self.ma50_rows)
        data.insert(0, "Ma_100", self.ma100_rows)
        data.insert(0, "Ma_200", self.ma200_rows)
        self.complete_data = data

    def moving_average_21(self):
        s = 0
        for i in self.ma21:
            s += i
        return s / 21
    def moving_average_50(self):
        s= 0
        for i in self.ma50:
            s+= i
        return s/50
    def moving_average_100(self):
        s= 0
        for i in self.ma100:
            s+= i
        return s/100
    def moving_average_200(self):
        s= 0
        for i in self.ma200:
            s+= i
        return s/200
    def get_all_ma(self):
        return self.complete_data
