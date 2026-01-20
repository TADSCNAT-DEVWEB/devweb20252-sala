"""
Settings para ambiente de desenvolvimento
"""

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-lhmqa4qaza^jv$10=$yfm8o&_%&5ado2tf_@gq88hem%s0mhf3" #Pode Mudar aqui

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Adicionar apps específicos de desenvolvimento
INSTALLED_APPS += [
    "debug_toolbar", #Não é obrigatório, só se tiver instalado
]

# Adicionar middlewares específicos de desenvolvimento
MIDDLEWARE.insert(4, "debug_toolbar.middleware.DebugToolbarMiddleware") #Se tiver instalado, adicionar

# Para servir arquivos estáticos com Gunicorn em desenvolvimento
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware') #Senão usar gunicorn, pode remover

# Database para desenvolvimento (SQLite)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Debug Toolbar
INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

# CSRF
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://localhost:8000', #Necessário para o codespace. Localmente não precisa
]

# Email backend para desenvolvimento (console) - Se tiver e-mail no sistema
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Configurações específicas para arquivos estáticos em desenvolvimento
# Permitir que o Gunicorn sirva arquivos estáticos via WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Para desenvolvimento, coletamos os arquivos estáticos automaticamente
import os
if not os.path.exists(BASE_DIR / 'staticfiles'):
    os.makedirs(BASE_DIR / 'staticfiles', exist_ok=True)

# Cache simples para desenvolvimento, se tiver opção de cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Logging para desenvolvimento, se necessário, podendo ser removido
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}