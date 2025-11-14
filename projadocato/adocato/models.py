from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Raca(models.Model):
    nome=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.nome

class Gato(models.Model):
    nome=models.CharField(max_length=100,verbose_name='Nome do Gato')
    sexo=models.CharField(max_length=1,choices=[('M','Macho'),('F','Femea')])
    cor=models.CharField(max_length=50)
    data_nascimento=models.DateField()
    descricao=models.TextField(blank=True,null=True)
    disponivel=models.BooleanField(default=True)
    raca=models.ForeignKey(Raca,on_delete=models.CASCADE,related_name='gatos')
    foto=models.ImageField(upload_to='gatos/',blank=True,null=True)

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
    class Meta:
        verbose_name='Gato'
        verbose_name_plural='Gatos'
        ordering=['nome']

class Usuario(User):
    cpf=models.CharField(max_length=11,unique=True)
    nome=models.CharField(max_length=150)

    def __str__(self):
        return self.nome
    class Meta:
        verbose_name='Usuário'
        verbose_name_plural='Usuários'

class Adotante(Usuario):
    telefone=models.CharField(max_length=15)
    foto=models.ImageField(upload_to='adotantes/',blank=True,null=True)

    class Meta:
        verbose_name='Adotante'
        verbose_name_plural='Adotantes'

class Coordenador(Usuario):
    apelido=models.CharField(max_length=50,unique=True)

    class Meta:
        verbose_name='Coordenador'
        verbose_name_plural='Coordenadores'

class Solicitacao(models.Model):
    adotante=models.ForeignKey(Adotante,on_delete=models.PROTECT,related_name='solicitacoes')
    gato=models.ForeignKey(Gato,on_delete=models.PROTECT,related_name='solicitacoes')
    criadaEM=models.DateTimeField(auto_now_add=True)
    recurso=models.TextField(blank=True,null=True)
    status=models.CharField(max_length=20,choices=[('EM_ANALISE','Em Análise'),('APROVADA','Aprovada'),('REPROVADA','Reprovada'),('EM_RECURSO','Em Recurso')],default='EM_ANALISE')
    avaliadores=models.ManyToManyField(Coordenador,related_name='avaliacoes',blank=True, through='Avaliacao')
    def __str__(self):
        return f'Solicitação de {self.adotante.nome} para {self.gato.nome}'
    
    class Meta:
        verbose_name='Solicitação'
        verbose_name_plural='Solicitações'
        ordering=['-criadaEM']

class Avaliacao(models.Model):
    solicitacao=models.ForeignKey(Solicitacao,on_delete=models.CASCADE)
    coordenador=models.ForeignKey(Coordenador,on_delete=models.CASCADE)
    parecer=models.TextField(blank=True,null=True)
    dataAvaliacao=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Avaliação de {self.coordenador.apelido} para {self.solicitacao}'
    
    class Meta:
        verbose_name='Avaliação'
        verbose_name_plural='Avaliações'
        ordering=['-dataAvaliacao']
class Documento(models.Model):
    solicitacao=models.ForeignKey(Solicitacao,on_delete=models.CASCADE,related_name='documentos')
    arquivo=models.FileField(upload_to='documentos/')
    descricao=models.CharField(max_length=200,blank=True,null=True)
    enviadoEM=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Documento para {self.solicitacao}'
    
    class Meta:
        verbose_name='Documento'
        verbose_name_plural='Documentos'
        ordering=['-enviadoEM']