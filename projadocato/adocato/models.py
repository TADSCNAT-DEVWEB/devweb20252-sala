from django.db import models

# Create your models here.

class Raca(models.Model):
    nome=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.nome

class Gato(models.Model):
    nome=models.CharField(max_length=100)
    sexo=models.CharField(max_length=1,choices=[('M','Macho'),('F','Femea')])
    cor=models.CharField(max_length=50)
    data_nascimento=models.DateField()
    descricao=models.TextField(blank=True,null=True)
    disponivel=models.BooleanField(default=True)
    raca=models.ForeignKey(Raca,on_delete=models.CASCADE,related_name='gatos')

    def __str__(self):
        return f'{self.nome} ({self.raca.nome})'

    @property
    def idade(self):
        from datetime import date
        hoje=date.today()
        idade=hoje.year - self.data_nascimento.year
        if (hoje.month,hoje.day) < (self.data_nascimento.month,self.data_nascimento.day):
            idade -= 1
        return idade