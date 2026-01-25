from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.home, name="home"),
    path("strategies", views.strategies, name="strategies"),
    path("<int:id>", views.equity, name="equity"),
]
