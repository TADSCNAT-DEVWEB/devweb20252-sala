from django.urls import path
from adocato.api.views import (
    RacaListCreateAPIView,
    RacaRetrieveUpdateDestroyAPIView
)

app_name = 'api'

urlpatterns = [
    path('racas/', RacaListCreateAPIView.as_view(), name='raca-list-create'),
    path('racas/<int:pk>/', RacaRetrieveUpdateDestroyAPIView.as_view(), name='raca-detail'),
]
