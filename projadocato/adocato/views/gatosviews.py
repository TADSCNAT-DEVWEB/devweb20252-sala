from django.views import View
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from adocato.services.gatoservice import GatoService
from adocato.services.racaservice import RacaService
from adocato.utils import GerenciadorMensagem
from adocato.views.mixins import CoordenadorMixin


class GatoListView(CoordenadorMixin,ListView):
    """View para listagem de gatos com filtros de busca"""
    template_name = 'adocato/gatos/lista.html'
    context_object_name = 'gatos'
    paginate_by = 9
    
    def get_queryset(self):
        nome = self.request.GET.get('nome', None)
        disponivel = self.request.GET.get('disponivel', None)
        
        # Converter string 'True'/'False' para booleano
        if disponivel == 'True':
            disponivel = True
        elif disponivel == 'False':
            disponivel = False
        else:
            disponivel = None
        
        return GatoService.buscar_gatos(nome=nome, disponivel=disponivel)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome'] = self.request.GET.get('nome', '')
        context['disponivel'] = self.request.GET.get('disponivel', '')
        return context


class GatoDisponivelListView(ListView):
    """View para listagem de gatos disponíveis para adoção"""
    template_name = 'adocato/gatos/disponiveis.html'
    context_object_name = 'gatos'
    paginate_by = 9
    
    def get_queryset(self):
        nome = self.request.GET.get('nome', None)
        return GatoService.buscar_gatos(nome=nome, disponivel=True)


class GatoDetailView(DetailView):
    """View para exibição detalhada de um gato"""
    template_name = 'adocato/gatos/detail.html'
    context_object_name = 'gato'
    
    def get_object(self, queryset=None):
        gato_id = self.kwargs.get('pk')
        gato = GatoService.obter_gato_por_id(gato_id)
        if not gato:
            from django.http import Http404
            raise Http404("Gato não encontrado")
        return gato


class GatoSalvarView(CoordenadorMixin, View):
    """View para cadastro e edição de gatos (apenas coordenadores)"""
    
    def get(self, request, gato_id=None):
        if gato_id:
            gato = GatoService.obter_gato_por_id(gato_id)
            if not gato:
                GerenciadorMensagem.processar_mensagem_erro(request, "Gato não encontrado.")
                return redirect('adocato:gato_list')
        else:
            gato = None
        
        racas = RacaService.listar_racas()
        context = {
            'gato': gato,
            'racas': racas
        }
        return render(request, 'adocato/gatos/form.html', context)
    
    def post(self, request, gato_id=None):
        nome = request.POST.get('nome')
        sexo = request.POST.get('sexo')
        cor = request.POST.get('cor')
        data_nascimento = request.POST.get('data_nascimento')
        raca_id = request.POST.get('raca')
        descricao = request.POST.get('descricao', '')
        foto = request.FILES.get('foto')
        
        try:
            if gato_id:
                # Atualização
                disponivel_str = request.POST.get('disponivel')
                disponivel = True if disponivel_str == '1' else False if disponivel_str == '0' else None
                
                gato = GatoService.atualizar_gato(
                    gato_id=gato_id,
                    nome=nome,
                    sexo=sexo,
                    cor=cor,
                    data_nascimento=data_nascimento,
                    raca_id=raca_id,
                    descricao=descricao,
                    foto=foto,
                    disponivel=disponivel
                )
                
                if gato:
                    GerenciadorMensagem.processar_mensagem_sucesso(request, 'Gato atualizado com sucesso!')
                else:
                    GerenciadorMensagem.processar_mensagem_erro(request, 'Gato não encontrado.')
            else:
                # Cadastro
                gato = GatoService.cadastrar_gato(
                    nome=nome,
                    sexo=sexo,
                    cor=cor,
                    data_nascimento=data_nascimento,
                    raca_id=raca_id,
                    descricao=descricao,
                    foto=foto
                )
                GerenciadorMensagem.processar_mensagem_sucesso(request, 'Gato cadastrado com sucesso!')
            
            return redirect('adocato:gato_list')
            
        except ValidationError as e:
            GerenciadorMensagem.processar_mensagem_erro(request, e)
            racas = RacaService.listar_racas()
            
            # Recuperar gato se for edição
            gato = None
            if gato_id:
                gato = GatoService.obter_gato_por_id(gato_id)
            
            context = {
                'gato': gato,
                'racas': racas
            }
            return render(request, 'adocato/gatos/form.html', context)


class GatoExcluirView(CoordenadorMixin, View):
    """View para exclusão de gatos (apenas coordenadores)"""
    
    def post(self, request, gato_id):
        sucesso = GatoService.excluir_gato(gato_id)
        
        if sucesso:
            GerenciadorMensagem.processar_mensagem_sucesso(request, 'Gato excluído com sucesso!')
        else:
            GerenciadorMensagem.processar_mensagem_erro(request, 'Gato não encontrado.')
        
        return redirect('adocato:gato_list')


class GatoPorRacaView(CoordenadorMixin,ListView):
    """View para listagem de gatos por raça"""
    template_name = 'adocato/gatos/por_raca.html'
    context_object_name = 'gatos'
    paginate_by = 9
    
    def get_queryset(self):
        raca_id = self.kwargs.get('raca_id')
        return GatoService.listar_gatos_por_raca(raca_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        raca_id = self.kwargs.get('raca_id')
        raca = RacaService.obter_raca_por_id(raca_id)
        context['raca'] = raca
        return context
