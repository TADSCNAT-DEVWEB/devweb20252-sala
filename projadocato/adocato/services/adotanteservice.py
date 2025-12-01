from adocato.models import Adotante
from django.core.exceptions import ValidationError

class AdotanteService:
   
    @staticmethod
    def buscar_adotantes(nome=None, cpf=None):
        adotantes = Adotante.objects.all()
        if nome:
            adotantes = adotantes.filter(nome__icontains=nome)
        if cpf:
            adotantes = adotantes.filter(cpf=cpf)
        return adotantes.order_by('nome')

    @staticmethod
    def listar_adotantes():
        return Adotante.objects.all().order_by('nome')

    @staticmethod
    def obter_adotante_por_id(adotante_id):
        try:
            return Adotante.objects.get(id=adotante_id)
        except Adotante.DoesNotExist:
            return None
    
    @staticmethod
    def obter_adotante_por_cpf(cpf):
        try:
            return Adotante.objects.get(cpf=cpf)
        except Adotante.DoesNotExist:
            return None
    
    @staticmethod
    def cadastrar_adotante(cpf, nome, username, password, email, data_nascimento, 
                          telefone, foto=None):
        adotante = Adotante(
            cpf=cpf,
            nome=nome,
            username=username,
            email=email,
            data_nascimento=data_nascimento,
            telefone=telefone,
            foto=foto
        )
        try:
            adotante.full_clean()
        except ValidationError as e:
            raise e
        adotante.set_password(password)
        adotante.save()
        return adotante
    
    @staticmethod
    def atualizar_adotante(adotante_id, cpf=None, nome=None, username=None, 
                          password=None, email=None, data_nascimento=None, 
                          telefone=None, foto=None):
        adotante = AdotanteService.obter_adotante_por_id(adotante_id)
        if not adotante:
            return None
        if cpf is not None:
            adotante.cpf = cpf
        if nome is not None:
            adotante.nome = nome
        if username is not None:
            adotante.username = username
        if email is not None:
            adotante.email = email
        if data_nascimento is not None:
            adotante.data_nascimento = data_nascimento
        if telefone is not None:
            adotante.telefone = telefone
        if foto is not None:
            adotante.foto = foto
        try:
            adotante.full_clean()
        except ValidationError as e:
            raise e
        if password is not None:
            adotante.set_password(password)
        adotante.save()
        return adotante
    
    @staticmethod
    def excluir_adotante(adotante_id):
        adotante = AdotanteService.obter_adotante_por_id(adotante_id)
        if not adotante:
            return False
        adotante.delete()
        return True
