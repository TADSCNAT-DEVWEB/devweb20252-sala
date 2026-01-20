# Esse arquivo precisa estar na pasta scripts dentro do seu projeto. Modifique para adaptar para a situação específica do projeto
import os
from django.contrib.auth import get_user_model

def run():

    User = get_user_model()
    username = 'professor'
    password = os.environ.get('ADMIN_PASSWORD')

    if not password:
        print("Erro: variável de ambiente ADMIN_PASSWORD não definida.")
        exit(1)

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, password=password)
        print(f"Superusuário '{username}' criado com sucesso.")
    else:
        print(f"Superusuário '{username}' já existe.")