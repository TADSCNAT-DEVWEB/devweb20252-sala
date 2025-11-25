from django.contrib import messages
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