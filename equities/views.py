from django.http import HttpResponse
from django.template import loader
import matplotlib.pyplot as plt
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
            "name":ticker["name"],
            "ticker":ticker["ticker"],
            "description":ticker["description"],
                       })
    context ={"data" : charts}
    print(context)
    return HttpResponse(template.render(context,request))
def strategies(request):
    global CACHE
    CACHE.check_last_update()
    template = loader.get_template('strategies.html')
    charts = []

    for ticker in CACHE.controller:

        ticker["data"].cumsum()
        ticker["data"].plot(y="Close")
        source = "equities/static/"+ticker["name"]+".png"
        plt.savefig(source)
        charts.append({
            "name":ticker["name"],
            "ticker":ticker["ticker"],
            "description":ticker["description"],
            "source":ticker["name"]+".png",
                       })
    context ={"data" : charts}
    print(CACHE.controller)
    return HttpResponse(template.render(context,request))

def home(request):
    template = loader.get_template("home.html")
    equities_data = Equity.objects.all()
    data = []
    for n in equities_data:
        temp = {
            "id":n.id,
            "name":n.name,
            "ticker": n.ticker,
            "description": n.description,
        }
        data.append(temp)
    context = {"data": data}
    return HttpResponse(template.render(context,request))

def equity(request,id):
    template = loader.get_template("equity.html")
    data = CACHE.controller[id]
    context = {"equity":data}
    return HttpResponse(template.render(context,request))