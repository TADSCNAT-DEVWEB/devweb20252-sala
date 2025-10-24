from django.http import JsonResponse
from django.shortcuts import render
from .services import Cidade,ClimaService

clima_service = ClimaService()
clima_service.inicializar_cidades()

# Create your views here.
def index(request):
    return render(request, "clima/index.html" )
def clima_view(request):
    nome_cidade=request.GET.get("nome_cidade")
    cidade = clima_service.obter_cidade(nome_cidade)
    if cidade:
        data = {
            "success": True,
            "nome_cidade": cidade.nome,
            "temperatura": cidade.clima.temperatura,
            "descricao": cidade.clima.descricao,
        }
        return JsonResponse(data)
    else:
        data = {
            "success": False,
            "erro": "Cidade não encontrada."
        }
        return JsonResponse(data, status=404)
