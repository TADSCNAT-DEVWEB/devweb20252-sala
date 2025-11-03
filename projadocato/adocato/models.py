from django.db import models

# Create your models here.

class Raca(models.Model):
    nome=models.CharField(max_length=100,unique=True)

class Gato(models.Model):
    nome=models.CharField(max_length=100)
    sexo=models.CharField(max_length=1,choices=[('M','Macho'),('F','Femea')])
    cor=models.CharField(max_length=50)
    data_nascimento=models.DateField()
    descricao=models.TextField(blank=True,null=True)
    disponivel=models.BooleanField(default=True)
    raca=models.ForeignKey(Raca,on_delete=models.CASCADE,related_name='gatos')
