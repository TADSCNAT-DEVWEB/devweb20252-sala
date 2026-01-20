from django import forms
class GatoForm(forms.Form):
    nome = forms.CharField(max_length=100, label='Nome do Gato')
    idade = forms.IntegerField(label='Idade do Gato')
    raca = forms.CharField(max_length=100, label='Raça do Gato')
    cor = forms.CharField(max_length=50, label='Cor do Gato')
    peso = forms.DecimalField(max_digits=5, decimal_places=2, label='Peso do Gato (kg)')
    foto = forms.ImageField(label='Foto do Gato', required=False)
    descricao = forms.CharField(widget=forms.Textarea, label='Descrição do Gato', required=False)

    def clean(self):
        return super().clean()