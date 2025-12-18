from django.urls import path
from django.views.generic import TemplateView
from adocato.views.indexviews import IndexView
from adocato.views.racaviews import RacaListView,RacaSalvarView,RacaExcluirView
from adocato.views.adotanteviews import AdotanteSalvarView, AdotanteDetailView
from adocato.views.gatosviews import GatoListView, GatoDisponivelListView, GatoDetailView
from . import views_old

app_name = 'adocato'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('racas/', RacaListView.as_view(), name='raca_list'),
    path('racas/cadastrar/', RacaSalvarView.as_view(), name='raca_cadastrar'),
    path('racas/<int:raca_id>/editar/', RacaSalvarView.as_view(), name='raca_editar'),
    path('racas/<int:raca_id>/excluir/', RacaExcluirView.as_view(), name='raca_excluir'),
    path('gatos/', views_old.gato_list, name='gato_list'),
    path('racas/<int:raca_id>/gatos/', views_old.gato_list_por_raca, name='gato_por_raca'),
    path('gatos/cadastrar/', views_old.gato_cadastrar, name='gato_cadastrar'),
    path('gatos/<int:gato_id>/editar/', views_old.gato_editar, name='gato_editar'),
    path('gatos/<int:gato_id>/excluir/', views_old.gato_excluir, name='gato_excluir'),
    path('gatos/disponiveis/', GatoDisponivelListView.as_view(), name='gatos_disponiveis'),
    path('adotantes/cadastrar/', AdotanteSalvarView.as_view(), name='adotante_cadastrar'),
    path('adotantes/meu_perfil/<int:pk>/', AdotanteDetailView.as_view(), name='adotante_meu_perfil'),
    path('login/', views_old.login_view, name='login'),
    path('logout/', views_old.logout_view, name='logout'),
]
