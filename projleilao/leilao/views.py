from django.shortcuts import render
from .models import Leilao, ItemLeilao
# Create your views here.

def index(request):
    leiloes = Leilao.objects.all()
    return render(request, 'leilao/index.html', {'leiloes': leiloes})

def exibir_itens_leilao(request, leilao_id):
    leilao = Leilao.objects.get(id=leilao_id)
    itens = leilao.itens.all()
    if request.method == 'POST':
        itens=itens.filter(titulo__icontains=request.POST.get('titulo',''))
    contexto={'leilao': leilao, 'itens': itens}
    return render(request, 'leilao/relatorio_leilao.html', contexto)
