
from adocato.services.racaservice import RacaService
from django.views.generic import ListView,View
from adocato.views.mixins import CoordenadorMixin,ExcluirRacaMixin
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from adocato.utils import GerenciadorMensagem
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required,name='dispatch')
class RacaListView(ListView):
    template_name = 'adocato/racas/lista.html'
    context_object_name = 'racas'
    paginate_by = 3
    
    def get_queryset(self):
        if self.request.GET.get('nome') is None:
            return RacaService.listar_racas()
        else:
            nome = self.request.GET.get('nome', '')
            return RacaService.buscar_racas(nome=nome)
    
    
    

    
@method_decorator(login_required,name='post')
class RacaSalvarView( View):
    def get(self, request, raca_id=None):
        if raca_id:
            raca = RacaService.obter_raca_por_id(raca_id)
        else:
            raca = None
        context = {'raca': raca}
        return render(request, 'adocato/racas/form.html', context)

    
    def post(self, request, raca_id=None):
        nome = request.POST.get('nome')
        try:
            if raca_id:
                RacaService.atualizar_raca(raca_id, nome)
                GerenciadorMensagem.processar_mensagem_sucesso(request, 'Raça atualizada com sucesso!')
            else:
                RacaService.cadastrar_raca(nome)
                GerenciadorMensagem.processar_mensagem_sucesso(request, 'Raça cadastrada com sucesso!')
            return redirect('adocato:raca_list')
        except ValidationError as e:
            GerenciadorMensagem.processar_mensagem_erro(request, e)
            return render(request, 'adocato/racas/form.html')
class RacaExcluirView(ExcluirRacaMixin, View):
    def post(self, request, raca_id):
        sucesso = RacaService.excluir_raca(raca_id)
        if sucesso:
            GerenciadorMensagem.processar_mensagem_sucesso(request, 'Raça excluída com sucesso!')
        else:
            GerenciadorMensagem.processar_mensagem_erro(request, 'Raça não encontrada.')
        return redirect('adocato:raca_list')