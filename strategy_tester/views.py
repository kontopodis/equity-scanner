from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from equities.models import Equity


# Create your views here.
def home(request):
    data = Equity.objects.all()

    template = loader.get_template("home.html")
    e = []
    for n in data:
        equity = {
            "name":n.name,
            "ticker":n.ticker,
            "description":n.description
        }
        e.append(equity)
    context = { "data" : e }
    return HttpResponse(template.render(context,request))