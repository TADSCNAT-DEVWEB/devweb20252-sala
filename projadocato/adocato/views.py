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

def gato_list_por_raca(request, raca_id):
    raca=Raca.objects.get(id=raca_id)
    gatos=Gato.objects.filter(raca=raca)
    context={'gatos':gatos}
    return render(request, 'adocato/gatos.html',context)

def gato_list(request):
    if request.method=='GET':
        gatos=Gato.objects.all()
    else:
        nome=request.POST.get('nome','')
        gatos=Gato.objects.filter(nome__icontains=nome)
        disponivel=request.POST.get('disponivel','')
        if disponivel=='1':
            gatos=gatos.filter(disponivel=True)
        elif disponivel=='0':
            gatos=gatos.filter(disponivel=False)
    context={'gatos':gatos}
    return render(request, 'adocato/gatos.html',context)
