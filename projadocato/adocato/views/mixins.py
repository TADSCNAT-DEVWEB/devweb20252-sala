from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from adocato.services.coordenadorservice import CoordenadorService
from adocato.services.adotanteservice import AdotanteService    
class CoordenadorMixin(UserPassesTestMixin):
    raise_exception = True
    def test_func(self):
        coordenador=CoordenadorService.obter_coordenador_por_id(self.request.user.id)
        return coordenador is not None

class AdotanteMixin(UserPassesTestMixin):
    raise_exception = True
    def test_func(self):
        adotante=AdotanteService.obter_adotante_por_id(self.request.user.id)
        return adotante is not None

class AdminMixin(UserPassesTestMixin):
    raise_exception = True
    def test_func(self):
        return self.request.user.is_superuser

class ExcluirRacaMixin(PermissionRequiredMixin):
    permission_required = 'raca.can_excluir'
    raise_exception = True
