from django.shortcuts import render,redirect
from .models import Raca, Gato
from adocato.services.gatoservice import GatoService
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
    gatos=GatoService.listar_gatos_por_raca(raca_id)
    context={'gatos':gatos}
    return render(request, 'adocato/gatos/lista.html',context)

def gato_cadastrar(request):
    racas=Raca.objects.all()
    if request.method=='POST':
        nome=request.POST.get('nome')
        sexo=request.POST.get('sexo')
        cor=request.POST.get('cor')
        data_nascimento=request.POST.get('data_nascimento')
        raca_id=request.POST.get('raca')
        descricao=request.POST.get('descricao','')
        foto=request.FILES.get('foto',None)
        GatoService.cadastrar_gato(nome, sexo, cor, data_nascimento, raca_id, descricao, foto)
        return redirect('adocato:gato_list')
    context={'racas':racas}
    return render(request, 'adocato/gatos/form.html',context)

def gato_editar(request, gato_id):
    gato=GatoService.obter_gato_por_id(gato_id)
    racas=Raca.objects.all()
    if not gato:
        return redirect('adocato:gato_list')
    if request.method=='POST':
        nome=request.POST.get('nome')
        sexo=request.POST.get('sexo')
        cor=request.POST.get('cor')
        data_nascimento=request.POST.get('data_nascimento')
        raca_id=request.POST.get('raca')
        descricao=request.POST.get('descricao','')
        foto=request.FILES.get('foto',None)
        disponivel=request.POST.get('disponivel','0')
        disponivel_bool = True if disponivel == '1' else False
        GatoService.atualizar_gato(gato_id,nome,sexo,cor,data_nascimento,raca_id,descricao,foto,disponivel_bool)
        return redirect('adocato:gato_list')
    context={'gato':gato,'racas':racas}
    return render(request, 'adocato/gatos/form.html',context)
def gato_list(request):
    if request.method=='GET':
        gatos=GatoService.buscar_gatos()
    else:
        nome=request.POST.get('nome','')
        disponivel=request.POST.get('disponivel','')
        if disponivel=='1':
            disponivel_bool = True
        elif disponivel=='0':
            disponivel_bool = False
        else:
            disponivel_bool = None
        gatos=GatoService.buscar_gatos(nome=nome, disponivel=disponivel_bool)
    context={'gatos':gatos}
    return render(request, 'adocato/gatos/lista.html',context)

def gato_excluir(request, gato_id):
    GatoService.excluir_gato(gato_id)
    return redirect('adocato:gato_list')

def listar_gatos_disponiveis(request):
    gatos=GatoService.listar_gatos_disponiveis()
    context={'gatos':gatos}
    return render(request, 'adocato/gatos/lista.html',context)