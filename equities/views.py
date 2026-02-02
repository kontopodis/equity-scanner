from django.http import HttpResponse
from django.template import loader
import matplotlib.pyplot as plt
from equities.strategies.st_builder import StrategyBuilder

from equities.controllers.cacheController import CacheController

CACHE = CacheController()
CACHE.update()
from equities.models import Equity


# Create your views here.
def index(request):
    global CACHE
    CACHE.check_last_update()
    template = loader.get_template("index.html")
    charts = []
    for ticker in CACHE.controller:
        charts.append({
            "name": ticker["name"],
            "ticker": ticker["ticker"],
        })
    context = {"data": charts}

    return HttpResponse(template.render(context, request))


def strategies(request):
    global CACHE
    CACHE.check_last_update()
    template = loader.get_template('strategies.html')
    results = []

    for ticker in CACHE.controller:
        st1 = StrategyBuilder(ticker["data"])
        st1.run()
        possible_trade = st1.check()
        text_possible_trade = "False"
        if possible_trade:
            text_possible_trade = "<b style='color:red;'>True</b>"
        chart_data = st1.data
        chart_data.cumsum()
        chart_data.plot(y=["Close",'active_trade','active_trade_loss','Pivot_points_s2','Pivot_points_r2'], grid=True, figsize=[15, 10])
        plt.savefig("equities/static/strategy_" + ticker["name"] + "_close.png")

        results.append({
            'name': ticker['name'],
            'description':st1.description,
            'stop_loss_counter': st1.stop_loss_counter,
            'take_profit_counter': st1.take_profit_counter,
            'stop_loss_result':st1.stop_loss_result,
            'take_profit_result': st1.take_profit_result,
            'possible_trade': text_possible_trade,
            "source_close": "/static/strategy_" + ticker["name"] + "_close.png",
            "id":ticker['id']
        })

    context = {"data": results}

    return HttpResponse(template.render(context, request))


def home(request):
    template = loader.get_template("home.html")
    equities_data = CACHE.controller
    data = []


    for n in equities_data:

        last_price = n["data"].tail(1)

        temp = {
            "id": n["id"],
            "name": n["name"],
            "ticker": n['ticker'],
            "close_price":round(last_price.iloc[0]['Close'],2),
            "open_price": round(last_price.iloc[0]['Open'],2),
            "low_price": round(last_price.iloc[0]['Low'],2),
            "high_price": round(last_price.iloc[0]['High'],2),
            "pivot_s2_price": round(last_price.iloc[0]['Pivot_points_s2'], 2),
            "pivot_s1_price": round(last_price.iloc[0]['Pivot_points_s1'], 2),
            "pivot_price": round(last_price.iloc[0]['Pivot_points'], 2),
            "pivot_r1_price": round(last_price.iloc[0]['Pivot_points_r1'], 2),
            "pivot_r2_price": round(last_price.iloc[0]['Pivot_points_r2'], 2),
            "vwap_high_price": round(last_price.iloc[0]['Vwap_high'], 2),
            "vwap_low_price": round(last_price.iloc[0]['Vwap_low'], 2),
            "ma50_price": round(last_price.iloc[0]['Ma_50'], 2),
            "ma100_price": round(last_price.iloc[0]['Ma_100'], 2),
            "ma200_price": round(last_price.iloc[0]['Ma_200'], 2),
        }
        data.append(temp)
    context = {"data": data}
    return HttpResponse(template.render(context, request))


def equity(request, id):
    template = loader.get_template("equity.html")
    all_equities = CACHE.controller
    data = {"name":"Wrong Id"}
    for e in all_equities:
        if id == e["id"]:
            data = e
            data["data"].cumsum()

            data["data"].plot(y="Close",grid=True,figsize=[15,10])
            plt.savefig("equities/static/" + data["name"] + "_close.png")
            data["source_close"] = "/static/" + data["name"] + "_close.png"

            data["data"].plot(y=["Close", "Vwap_low", "Vwap_high"], grid=True,figsize=[15,10])
            plt.savefig("equities/static/"+data["name"]+"_vwap.png")
            data["source_vwap"] = "/static/"+data["name"]+"_vwap.png"


            data["data"].plot(y=["Close", "Ma_50","Ma_100","Ma_200"], grid=True,figsize=[15,10])
            plt.savefig("equities/static/"+data["name"]+"_moving_averages.png")
            data["source_moving_averages"] = "/static/"+data["name"]+"_moving_averages.png"


            data["data"].plot(y=["Close", "Pivot_points","Pivot_points_r2","Pivot_points_s2"], grid=True,figsize=[15,10])
            plt.savefig("equities/static/"+data["name"]+"_pivot_points.png")
            data["source_pivot_points"] = "/static/"+data["name"]+"_pivot_points.png"

            mo12_data = e
            mo12_data["mo12_data"].plot(y="Close",grid=True,figsize=[15,10])
            plt.savefig("equities/static/mo12_" + data["name"] + "_close.png")
            mo12_data["source_close_mo12"] = "/static/mo12_" + data["name"] + "_close.png"

            mo12_data["mo12_data"].plot(y=["Close", "Vwap_low", "Vwap_high"], grid=True,figsize=[15,10])
            plt.savefig("equities/static/mo12_"+data["name"]+"_vwap.png")
            data["source_vwap_mo12"] = "/static/mo12_"+data["name"]+"_vwap.png"


            mo12_data["mo12_data"].plot(y=["Close", "Ma_50","Ma_100","Ma_200"], grid=True,figsize=[15,10])
            plt.savefig("equities/static/mo12_"+data["name"]+"_moving_averages.png")
            mo12_data["source_moving_averages_mo12"] = "/static/mo12_"+data["name"]+"_moving_averages.png"







    context = {"equity": data}
    return HttpResponse(template.render(context, request))
