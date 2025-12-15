
from django import forms
from django.forms import Form
class AdotanteForm(Form):
    username=forms.CharField(max_length=150,label='Nome de Usuário')
    password=forms.CharField(max_length=128,label='Senha',widget=forms.PasswordInput)
    nome=forms.CharField(max_length=150,label='Nome Completo')
    cpf=forms.CharField(max_length=11,label='CPF')
    email=forms.EmailField(label='Email')
    data_nascimento=forms.DateField(label='Data de Nascimento',widget=forms.DateInput(attrs={'type':'date'}),required=False)
    telefone=forms.CharField(max_length=15,label='Telefone')
    foto=forms.ImageField(label='Foto',required=False)

    def clean(self):
        return super().clean()
