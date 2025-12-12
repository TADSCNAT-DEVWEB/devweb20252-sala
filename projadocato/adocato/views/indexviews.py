from django.views.generic import TemplateView
class IndexView(TemplateView):
    template_name = 'adocato/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mensagem']='Bem-vindo ao Adocato!!!!!'
        return context