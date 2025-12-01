from django.contrib import messages
from adocato.services.coordenadorservice import CoordenadorService
from adocato.services.adotanteservice import AdotanteService
class GerenciadorMensagem:
    @staticmethod
    def processar_mensagem_erro(request,validation_error):
   # Lista para armazenar mensagens únicas
        mensagens_unicas = set()
        
        if hasattr(validation_error, 'message_dict') and validation_error.message_dict:
            # Erros estruturados por campo
            for campo, erros in validation_error.message_dict.items():
                if isinstance(erros, list):
                    for erro in erros:
                        mensagem = f'{campo.title()}: {erro}'
                        mensagens_unicas.add(mensagem)
                else:
                    mensagem = f'{campo.title()}: {erros}'
                    mensagens_unicas.add(mensagem)
        elif hasattr(validation_error, 'messages') and validation_error.messages:
            # Lista de mensagens de erro
            for mensagem in validation_error.messages:
                mensagens_unicas.add(str(mensagem))
        else:
            # Mensagem simples
            mensagens_unicas.add(str(validation_error))
        
        # Adiciona apenas mensagens únicas
        for mensagem in mensagens_unicas:
            messages.error(request, mensagem)
    
    @staticmethod
    def processar_mensagem_sucesso(request, mensagem):
        if isinstance(mensagem, str):
            messages.success(request, mensagem)
        elif isinstance(mensagem, list):
            # Remove duplicatas da lista
            mensagens_unicas = list(set(mensagem))
            for msg in mensagens_unicas:
                messages.success(request, msg)
        else:
            raise ValueError("A mensagem deve ser uma string ou uma lista de strings.")

class GerenciadorSessaoUsuario:
    @staticmethod
    def determinar_tipo_usuario(request):
        """
        Determina o tipo de usuário (adotante ou coordenador) e armazena na sessão.
        Retorna um dicionário com informações do usuário.
        """
        if not request.user.is_authenticated:
            return {
                'tipo_usuario': 'anonimo',
                'eh_adotante': False,
                'eh_coordenador': False,
                'eh_administrador': False,
                'usuario_nome': None,
                'usuario_id': None
            }
        
        # Verifica se já existe na sessão e se é para o mesmo usuário
        sessao_key = f'tipo_usuario_{request.user.id}'
        if sessao_key in request.session:
            return request.session[sessao_key]
        
        
        # Verifica se é adotante
        adotante = AdotanteService.obter_adotante_por_id(request.user.id)
        if adotante:
            info_usuario = {
                'tipo_usuario': 'adotante',
                'eh_adotante': True,
                'eh_coordenador': False,
                'eh_administrador': False,
                'usuario_nome': adotante.nome,
                'usuario_id': adotante.id,
                'usuario_email': adotante.email,
                'usuario_username': adotante.username
            }
        else:
            # Verifica se é coordenador
            coordenador = CoordenadorService.obter_coordenador_por_id(request.user.id)
            if coordenador:
                info_usuario = {
                    'tipo_usuario': 'coordenador',
                    'eh_adotante': False,
                    'eh_coordenador': True,
                    'eh_administrador': False,
                    'usuario_nome': coordenador.nome,
                    'usuario_id': coordenador.id,
                    'usuario_email': coordenador.email,
                    'usuario_username': coordenador.username
                }
            else:
                # Usuário logado mas sem tipo específico, nesse caso, é um administrador
                info_usuario = {
                    'tipo_usuario': 'administrador',
                    'eh_adotante': False,
                    'eh_coordenador': False,
                    'eh_administrador': True,
                    'usuario_nome': request.user.username,
                    'usuario_id': request.user.id,
                    'usuario_email': request.user.email,
                    'usuario_username': request.user.username
                }
        
        # Armazena na sessão
        request.session[sessao_key] = info_usuario
        request.session['usuario_nome'] = info_usuario['usuario_nome'] # Armazena o nome do usuário(login) na sessão
        return info_usuario
    
    @staticmethod
    def limpar_sessao_usuario(request):
        """Remove as informações do usuário da sessão."""
        if request.user.is_authenticated:
            sessao_key = f'tipo_usuario_{request.user.id}'
            if sessao_key in request.session:
                del request.session[sessao_key]