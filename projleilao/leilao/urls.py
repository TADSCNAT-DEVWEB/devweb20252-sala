from django.urls import path
from . import views
app_name = 'leilao'
urlpatterns = [
    path('', views.index, name='index'),
    path('leilao/<int:leilao_id>/', views.exibir_itens_leilao, name='exibir_itens_leilao'),
]
