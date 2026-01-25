from datetime import datetime
from equities.controllers.tickerController import TickerController
from equities.models import Equity
class CacheController:
    def __init__(self):
        self.controller = []
        self.last_update = datetime.today()
    def add_equity(self,equity):
        self.controller.append(equity)

    def clear_all(self):
        self.controller.clear()

    def check_last_update(self):
        print(self.last_update.date(), " - ",datetime.today().date())
        if self.last_update.date() == datetime.today().date():
            print(self.controller)
            print("Cache didn't update")
        else:

            self.update()
            print("Cache updated")

    def update(self):
        ## I have to put here the updates
        equities = Equity.objects.all()
        for e in equities:

            ticker = TickerController(e.ticker)
            self.add_equity({
                "id":e.id,
                "data":ticker.get_5year_data(),
                "name":e.name,
                "ticker":e.ticker,
                "description":ticker.get_description()
            })


