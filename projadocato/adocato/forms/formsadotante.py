
from django import forms
from django.forms import Form
class AdotanteForm(Form):
    username=forms.CharField(max_length=150,label='Nome de Usuário')
    password=forms.CharField(max_length=128,label='Senha',widget=forms.PasswordInput)
    confirm_password=forms.CharField(max_length=128,label='Confirmar Senha',widget=forms.PasswordInput)
    nome=forms.CharField(max_length=150,label='Nome Completo')
    cpf=forms.CharField(max_length=11,label='CPF')
    email=forms.EmailField(label='Email')
    data_nascimento=forms.DateField(label='Data de Nascimento',widget=forms.DateInput(attrs={'type':'date'}),required=False)
    telefone=forms.CharField(max_length=15,label='Telefone')
    foto=forms.ImageField(label='Foto',required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password:
            if password != confirm_password:
                self.add_error('password', 'As senhas não coincidem')
                self.add_error('confirm_password', 'As senhas não coincidem')
        else:
            self.add_error('password', 'A senha é obrigatória')
            self.add_error('confirm_password', 'A confirmação de senha é obrigatória')
        return cleaned_data
