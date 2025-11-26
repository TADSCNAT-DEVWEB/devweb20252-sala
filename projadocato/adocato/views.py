from django.shortcuts import render,redirect
from .models import Raca, Gato
from django.core.exceptions import ValidationError
from adocato.services.gatoservice import GatoService
from adocato.services.racaservice import RacaService
from adocato.utils import GerenciadorMensagem
# Create your views here.

def index(request):
    return render(request, 'adocato/index.html')

def raca_list(request):
    if request.method=='GET':
        racas=RacaService.listar_racas()
    else:
        nome=request.POST.get('nome','')
        racas=RacaService.buscar_racas(nome=nome)
    context={'racas':racas}
    return render(request, 'adocato/racas/lista.html',context)

def gato_list_por_raca(request, raca_id):
    gatos=GatoService.listar_gatos_por_raca(raca_id)
    context={'gatos':gatos}
    return render(request, 'adocato/gatos/lista.html',context)

def gato_cadastrar(request):
    racas=RacaService.listar_racas()
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
    racas=RacaService.listar_racas()
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
        try:
            GatoService.atualizar_gato(gato_id,nome,sexo,cor,data_nascimento,raca_id,descricao,foto,disponivel_bool)
            GerenciadorMensagem.processar_mensagem_sucesso(request, 'Gato atualizado com sucesso!')
            return redirect('adocato:gato_list')
        except ValidationError as e:
            GerenciadorMensagem.processar_mensagem_erro(request, e)
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
    GerenciadorMensagem.processar_mensagem_sucesso(request, 'Gato excluído com sucesso!')
    return redirect('adocato:gato_list')

def listar_gatos_disponiveis(request):
    gatos=GatoService.listar_gatos_disponiveis()
    context={'gatos':gatos}
    return render(request, 'adocato/gatos/lista.html',context)

def raca_cadastrar(request):
    if request.method=='POST':
        nome=request.POST.get('nome')
        try:
            RacaService.cadastrar_raca(nome)
            GerenciadorMensagem.processar_mensagem_sucesso(request, 'Raça cadastrada com sucesso!')
            return redirect('adocato:raca_list')
        except ValidationError as e:
            GerenciadorMensagem.processar_mensagem_erro(request, e)
    return render(request, 'adocato/racas/form.html')

def raca_editar(request, raca_id):
    raca=RacaService.obter_raca_por_id(raca_id)
    if not raca:
        return redirect('adocato:raca_list')
    if request.method=='POST':
        nome=request.POST.get('nome')
        try:
            RacaService.atualizar_raca(raca_id, nome)
            GerenciadorMensagem.processar_mensagem_sucesso(request, 'Raça atualizada com sucesso!')
            return redirect('adocato:raca_list')
        except ValidationError as e:
            GerenciadorMensagem.processar_mensagem_erro(request, e)
    context={'raca':raca}
    return render(request, 'adocato/racas/form.html',context)

def raca_excluir(request, raca_id):
    RacaService.excluir_raca(raca_id)
    GerenciadorMensagem.processar_mensagem_sucesso(request, 'Raça excluída com sucesso!')
    return redirect('adocato:raca_list')