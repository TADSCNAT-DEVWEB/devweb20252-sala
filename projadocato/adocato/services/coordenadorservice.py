from adocato.models import Coordenador
from django.core.exceptions import ValidationError

class CoordenadorService:
   
    @staticmethod
    def buscar_coordenadores(nome=None, apelido=None):
        coordenadores = Coordenador.objects.all()
        if nome:
            coordenadores = coordenadores.filter(nome__icontains=nome)
        if apelido:
            coordenadores = coordenadores.filter(apelido__icontains=apelido)
        return coordenadores.order_by('nome')

    @staticmethod
    def listar_coordenadores():
        return Coordenador.objects.all().order_by('nome')

    @staticmethod
    def obter_coordenador_por_id(coordenador_id):
        try:
            return Coordenador.objects.get(id=coordenador_id)
        except Coordenador.DoesNotExist:
            return None
    
    @staticmethod
    def obter_coordenador_por_apelido(apelido):
        try:
            return Coordenador.objects.get(apelido=apelido)
        except Coordenador.DoesNotExist:
            return None
    
    @staticmethod
    def obter_coordenador_por_cpf(cpf):
        try:
            return Coordenador.objects.get(cpf=cpf)
        except Coordenador.DoesNotExist:
            return None
    
    @staticmethod
    def cadastrar_coordenador(cpf, nome, username, password, email, apelido):
        coordenador = Coordenador(
            cpf=cpf,
            nome=nome,
            username=username,
            email=email,
            apelido=apelido
        )
        try:
            coordenador.full_clean()
        except ValidationError as e:
            raise e
        coordenador.set_password(password)
        coordenador.save()
        return coordenador
    
    @staticmethod
    def atualizar_coordenador(coordenador_id, cpf=None, nome=None, username=None, 
                            password=None, email=None, apelido=None):
        coordenador = CoordenadorService.obter_coordenador_por_id(coordenador_id)
        if not coordenador:
            return None
        if cpf is not None:
            coordenador.cpf = cpf
        if nome is not None:
            coordenador.nome = nome
        if username is not None:
            coordenador.username = username
        if email is not None:
            coordenador.email = email
        if apelido is not None:
            coordenador.apelido = apelido
        try:
            coordenador.full_clean()
        except ValidationError as e:
            raise e
        if password is not None:
            coordenador.set_password(password)
        coordenador.save()
        return coordenador
    
    @staticmethod
    def excluir_coordenador(coordenador_id):
        coordenador = CoordenadorService.obter_coordenador_por_id(coordenador_id)
        if not coordenador:
            return False
        coordenador.delete()
        return True
