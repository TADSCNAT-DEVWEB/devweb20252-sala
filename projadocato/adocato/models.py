from datetime import datetime,date
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.

class Raca(models.Model):
    nome=models.CharField(max_length=100,unique=True)

    def clean(self):
        erros={}
        if len(self.nome)<3:
            erros['nome']='O nome da raça deve ter pelo menos 3 caracteres.'
        if erros:
            raise ValidationError(erros)

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

    def clean(self):
        erros={}
        if len(self.nome)<5:
            erros['nome']='O nome do gato deve ter pelo menos 5 caracteres.'
        if not self.cor:
            erros['cor']='A cor do gato é obrigatória.'
        if self.sexo not in ['M','F']:
            erros['sexo']='O sexo deve ser "M" para macho ou "F" para fêmea.'
        if not self.data_nascimento:
            erros['data_nascimento']='A data de nascimento é obrigatória.'
        if self.data_nascimento>date.today():
            erros['data_nascimento']='A data de nascimento não pode ser no futuro.'
        if erros:
            raise ValidationError(erros)

    @property
    def idade(self):
        if not self.data_nascimento:
            return 0
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

    def clean(self):
        erros={}
        if len(self.nome)<5:
            erros['nome']='O nome completo deve ter pelo menos 5 caracteres.'
        if len(self.cpf)!=11 or not self.cpf.isdigit():
            erros['cpf']='O CPF deve conter exatamente 11 dígitos numéricos.'
        if len(self.username)<5:
            erros['username']='O nome de usuário deve ter pelo menos 5 caracteres.'
        if len(self.password)<6:
            erros['password']='A senha deve ter pelo menos 6 caracteres.'
        if erros:
            raise ValidationError(erros)

    def __str__(self):
        return self.nome
    
    def cpf_formatado(self):
        return f'{self.cpf[:3]}.{self.cpf[3:6]}.{self.cpf[6:9]}-{self.cpf[9:]}'
    class Meta:
        verbose_name='Usuário'
        verbose_name_plural='Usuários'

class Adotante(Usuario):
    data_nascimento=models.DateField(null=True,blank=True)
    telefone=models.CharField(max_length=15)
    foto=models.ImageField(upload_to='adotantes/',blank=True,null=True)

    class Meta:
        verbose_name='Adotante'
        verbose_name_plural='Adotantes'
    
    @property
    def idade(self):
        if not self.data_nascimento:
            return 0
        hoje=date.today()
        idade=hoje.year - self.data_nascimento.year
        if (hoje.month,hoje.day) < (self.data_nascimento.month,self.data_nascimento.day):
            idade -= 1
        return idade

    def clean(self):
        erros={}
        try :
            super().clean()
        except ValidationError as e:
            erros.update(e.message_dict) #Inclui a validação da superclasse dentro da estrutura de validação atual
        if not self.data_nascimento:
            erros['data_nascimento']='A data de nascimento é obrigatória.'
        if self.data_nascimento>date.today():
            erros['data_nascimento']='A data de nascimento não pode ser no futuro.'
        if self.idade<18:
            erros['data_nascimento']='O adotante deve ter pelo menos 18 anos.'
        if erros:
            raise ValidationError(erros)

class Coordenador(Usuario):
    apelido=models.CharField(max_length=50,unique=True)

    def clean(self):
        erros={}
        try:
            super().clean()
        except ValidationError as e:
            erros.update(e.message_dict) #Inclui a validação da superclasse dentro da estrutura de validação atual
        if len(self.apelido)<3:
            erros['apelido']='O apelido deve ter pelo menos 3 caracteres.'
        if erros:
            raise ValidationError(erros)

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
    
    def clean(self):
        erros={}
        if self.gato and not self.gato.disponivel:
            erros['gato']='O gato selecionado não está disponível para adoção.'
        if not self.adotante:
            erros['adotante']='A/O adotante é obrigatória.'
        if erros:
            raise ValidationError(erros)

    @property
    def atrasada(self):
        prazo_analise=7
        dias_decorridos=(datetime.now()-self.criadaEM).days
        return dias_decorridos>prazo_analise

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