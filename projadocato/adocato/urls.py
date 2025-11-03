from django.urls import path
from . import views

app_name = 'adocato'

urlpatterns = [
    path('', views.index, name='index'),
    path('racas/', views.raca_list, name='raca_list'),
    path('gatos/', views.gato_list, name='gato_list'),
]
