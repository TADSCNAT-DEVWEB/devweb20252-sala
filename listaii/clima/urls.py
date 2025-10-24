from django.contrib import admin
from django.urls import path
from .views import clima_view,index
app_name = "clima"
urlpatterns = [
   path("", index, name="index"),
   path("clima/", clima_view, name="clima"),
]