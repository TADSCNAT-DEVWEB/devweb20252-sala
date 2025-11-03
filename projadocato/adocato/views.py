from django.shortcuts import render
from .models import Raca, Gato

# Create your views here.

def index(request):
    return render(request, 'adocato/index.html')
def raca_list(request):
    if request.method=='GET':
        racas=Raca.objects.all()
    else:
        nome=request.POST.get('nome','')
        racas=Raca.objects.filter(nome__icontains=nome)
    context={'racas':racas}
    return render(request, 'adocato/racas.html',context)
def gato_list(request):
    gatos=Gato.objects.all()
    context={'gatos':gatos}
    return render(request, 'adocato/gato_list.html',context)
