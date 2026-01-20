#!/usr/bin/env bash
# exit on error
set -o errexit

# Change to project directory
#cd xxx # Diretório do projeto

# Install dependencies
pip install -r requirements_render.txt

# Collect static files
python manage.py collectstatic --noinput --settings=projadocato.settings.production # Coloque o nome do projeto

# Run migrations
python manage.py migrate --settings=projadocato.settings.production # Coloque o nome do projeto

#Cria um superusuário com a senha definida no ambiente
python manage.py runscript createsuperuser --settings=projadocato.settings.production #Coloque o nome do projeto
