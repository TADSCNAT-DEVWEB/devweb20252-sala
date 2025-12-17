
from django.views import View
from django.views.generic.detail import DetailView
from adocato.forms.formsadotante import AdotanteForm
from adocato.services.adotanteservice import AdotanteService
from django.shortcuts import redirect,render
from django.core.exceptions import ValidationError
from adocato.utils import GerenciadorMensagem
from adocato.views.mixins import AdotanteMixin


class AdotanteDetailView(AdotanteMixin, DetailView):
    
    template_name = 'adocato/adotantes/detail.html'
    context_object_name = 'adotante'

    def get_object(self, queryset = ...):
        
        return AdotanteService.obter_adotante_por_id(self.kwargs['pk'])

class AdotanteSalvarView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('adocato:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form_adotante = AdotanteForm()
        return render(request, 'adocato/adotantes/form.html', {'form': form_adotante})

    def post(self, request, *args, **kwargs):
        form_adotante = AdotanteForm(request.POST, request.FILES)
        if form_adotante.is_valid():
            dados = form_adotante.cleaned_data
            try:
                adotante = AdotanteService.cadastrar_adotante(
                    cpf=dados['cpf'],
                    nome=dados['nome'],
                    username=dados['username'],
                    password=dados['password'],
                    email=dados['email'],
                    data_nascimento=dados['data_nascimento'],
                    telefone=dados['telefone'],
                    foto=dados.get('foto')
                )
                GerenciadorMensagem.processar_mensagem_sucesso(request, "Adotante cadastrado com sucesso.")
                return redirect('adocato:index')
            except ValidationError as e:
                # Processa erro adicionando ao messages E ao formulário
                GerenciadorMensagem.processar_mensagem_erro(request, e, form=form_adotante)
        return render(request, 'adocato/adotantes/form.html', {'form': form_adotante})