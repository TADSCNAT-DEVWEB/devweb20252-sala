from django.urls import path
from adocato.api.views import (
    RacaListCreateAPIView,
    RacaRetrieveUpdateDestroyAPIView,
    #GatoListCreateAPIView,
    #GatoRetrieveUpdateDestroyAPIView
)

app_name = 'api'

urlpatterns = [
    path('racas/', RacaListCreateAPIView.as_view(), name='raca-list-create'),
    path('racas/<int:pk>/', RacaRetrieveUpdateDestroyAPIView.as_view(), name='raca-detail'),
    #path('gatos/', GatoListCreateAPIView.as_view(), name='gato-list-create'),
    #path('gatos/<int:pk>/', GatoRetrieveUpdateDestroyAPIView.as_view(), name='gato-detail'),
]
