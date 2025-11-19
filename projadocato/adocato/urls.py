from django.urls import path
from . import views

app_name = 'adocato'

urlpatterns = [
    path('', views.index, name='index'),
    path('racas/', views.raca_list, name='raca_list'),
    path('gatos/', views.gato_list, name='gato_list'),
    path('racas/<int:raca_id>/gatos/', views.gato_list_por_raca, name='gato_por_raca'),
    path('gatos/cadastrar/', views.gato_cadastrar, name='gato_cadastrar'),
    path('gatos/<int:gato_id>/editar/', views.gato_editar, name='gato_editar'),
    path('gatos/<int:gato_id>/excluir/', views.gato_excluir, name='gato_excluir'),
    path('gatos/disponiveis/', views.listar_gatos_disponiveis, name='gatos_disponiveis'),
]
