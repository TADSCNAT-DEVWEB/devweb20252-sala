from adocato.models import Gato,Raca
from django.core.exceptions import ValidationError
class GatoService:
   
    @staticmethod
    def buscar_gatos(nome=None, disponivel=None):
        gatos = Gato.objects.all()
        if nome:
            gatos = gatos.filter(nome__icontains=nome)
        if disponivel is not None:
            gatos = gatos.filter(disponivel=disponivel)
        return gatos.order_by('nome')

    @staticmethod
    def listar_gatos_por_raca(raca_id):
        return Gato.objects.filter(raca__id=raca_id).order_by('nome')

    @staticmethod
    def listar_gatos_disponiveis():
        return Gato.objects.filter(disponivel=True).order_by('nome')

    @staticmethod
    def obter_gato_por_id(gato_id):
        try:
            return Gato.objects.get(id=gato_id)
        except Gato.DoesNotExist:
            return None
    
    @staticmethod
    def cadastrar_gato(nome, sexo, cor, data_nascimento, raca_id, descricao=None, foto=None):
        gato = Gato(
            nome=nome,
            sexo=sexo,
            cor=cor,
            data_nascimento=data_nascimento,
            raca=Raca.objects.get(id=raca_id),
            descricao=descricao,
            foto=foto,
            disponivel=True
        )
        try:
            gato.full_clean()
        except ValidationError as e:
            raise e
        gato.save()
        return gato
    @staticmethod
    def atualizar_gato(gato_id,nome=None,sexo=None,cor=None,data_nascimento=None,raca_id=None,descricao=None,foto=None,disponivel=None):
        gato=GatoService.obter_gato_por_id(gato_id)
        if not gato:
            return None
        if nome is not None:
            gato.nome=nome
        if sexo is not None:
            gato.sexo=sexo
        if cor is not None:
            gato.cor=cor
        if data_nascimento is not None:
            gato.data_nascimento=data_nascimento
        if raca_id is not None:
            gato.raca=Raca.objects.get(id=raca_id)
        if descricao is not None:
            gato.descricao=descricao
        if foto is not None:
            gato.foto=foto
        if disponivel is not None:
            gato.disponivel=disponivel
        try:
            gato.full_clean()
        except ValidationError as e:
            raise e
        gato.save()
        return gato
    @staticmethod
    def excluir_gato(gato_id):
        gato=GatoService.obter_gato_por_id(gato_id)
        if not gato:
            return False
        gato.delete()
        return True
    