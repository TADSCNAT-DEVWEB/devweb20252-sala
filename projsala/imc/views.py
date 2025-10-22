from django.shortcuts import render,redirect
from django.template.loader import render_to_string
import json 
from django.http import HttpResponse
from .services import IMCService
# Create your views here.​

def index(request):
    return render(request,'index.html')
def nome(request):
    return HttpResponse("<h1>André Gustavo Duarte</h1>")
def calcular_imc(request):
    if request.method == 'GET':
        return redirect('imc:index')
    dados= json.loads(request.body) #Agora o conteúdo é JSON, o que precisa ser convertido para um dicionário
    altura = float(dados['altura'])
    peso = float(dados['peso'])
    imc,classificacao = IMCService.calcular_imc(peso, altura)
    contexto={
        'imc':f'{imc:.2f}',
        'classificacao':classificacao,
        'altura':altura,
        'peso':peso
    }
    html= render_to_string('resultado_imc.html', contexto) #A função render_to_string renderiza o template e retorna o HTML como string
    return HttpResponse(html)
def tabuada(request, numero):
    html=f'<table border="1"><tr><td>Tabuada de {numero}</td></tr>'
    for i in range(1,11):
        html+=f'<tr><td>{i} x {numero} = {i*numero}</td></tr>'
    html+='</table>'
    return HttpResponse(html)