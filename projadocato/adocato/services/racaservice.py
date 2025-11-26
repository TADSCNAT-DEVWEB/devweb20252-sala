from adocato.models import Raca
from django.core.exceptions import ValidationError

class RacaService:
   
    @staticmethod
    def buscar_racas(nome=None):
        racas = Raca.objects.all()
        if nome:
            racas = racas.filter(nome__icontains=nome)
        return racas.order_by('nome')

    @staticmethod
    def listar_racas():
        return Raca.objects.all().order_by('nome')

    @staticmethod
    def obter_raca_por_id(raca_id):
        try:
            return Raca.objects.get(id=raca_id)
        except Raca.DoesNotExist:
            return None
    
    @staticmethod
    def cadastrar_raca(nome):
        raca = Raca(nome=nome)
        try:
            raca.full_clean()
        except ValidationError as e:
            raise e
        raca.save()
        return raca
    
    @staticmethod
    def atualizar_raca(raca_id, nome=None):
        raca = RacaService.obter_raca_por_id(raca_id)
        if not raca:
            return None
        if nome is not None:
            raca.nome = nome
        try:
            raca.full_clean()
        except ValidationError as e:
            raise e
        raca.save()
        return raca
    
    @staticmethod
    def excluir_raca(raca_id):
        raca = RacaService.obter_raca_por_id(raca_id)
        if not raca:
            return False
        raca.delete()
        return True
