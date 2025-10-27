from django.shortcuts import render

# Create your views here.

def index(request):
    """
    View para a página inicial do projeto.
    Demonstra o uso de herança de templates.
    """
    context = {
        'titulo': 'Página Inicial',
        'descricao': 'Sistema de demonstração de templates Django com Bulma CSS'
    }
    return render(request, 'principal/index.html', context)
