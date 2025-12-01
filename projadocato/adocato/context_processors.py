from adocato.utils import GerenciadorSessaoUsuario

def usuario_context(request):
    return GerenciadorSessaoUsuario.determinar_tipo_usuario(request)