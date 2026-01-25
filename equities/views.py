from django.http import HttpResponse
from django.template import loader
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import figimage
from numpy.ma.core import size

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
            "description": ticker["description"],
        })
    context = {"data": charts}
    print(context)
    return HttpResponse(template.render(context, request))


def strategies(request):
    global CACHE
    CACHE.check_last_update()
    template = loader.get_template('strategies.html')
    charts = []

    for ticker in CACHE.controller:
        ticker["data"].cumsum()
        ticker["data"].plot(y="Close")
        source = "equities/static/" + ticker["name"] + ".png"
        plt.savefig(source)
        charts.append({
            "name": ticker["name"],
            "ticker": ticker["ticker"],
            "description": ticker["description"],
            "source": ticker["name"] + ".png",
        })
    context = {"data": charts}
    print(CACHE.controller)
    return HttpResponse(template.render(context, request))


def home(request):
    template = loader.get_template("home.html")
    equities_data = Equity.objects.all()
    data = []
    for n in equities_data:

        temp = {
            "id": n.id,
            "name": n.name,
            "ticker": n.ticker,
            "description": n.description,
        }
        data.append(temp)
    context = {"data": data}
    return HttpResponse(template.render(context, request))


def equity(request, id):
    template = loader.get_template("equity.html")
    all_equities = CACHE.controller
    data = {"name":"Wrong Id"}
    for e in all_equities:
        print( e["id"], id)
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




    context = {"equity": data}
    return HttpResponse(template.render(context, request))
