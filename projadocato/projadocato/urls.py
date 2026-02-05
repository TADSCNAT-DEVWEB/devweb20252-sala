"""
URL configuration for projadocato project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf.urls.static import static
import os

# Configuração dinâmica da URL base para o Swagger no Codespace
def get_swagger_base_url():
    if 'CODESPACE_NAME' in os.environ:
        codespace_name = os.getenv("CODESPACE_NAME")
        codespace_domain = os.getenv("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN", "github.dev")
        return f'https://{codespace_name}-8000.{codespace_domain}'
    return None

# Configuração do Schema para Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Adocato API",
        default_version='v1',
        description="API REST para o sistema de adoção de gatos",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contato@adocato.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=get_swagger_base_url(),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("adocato.urls")),
    path("api/",include("adocato.api.urls")),
    path("accounts/",include("django.contrib.auth.urls")),
    # Swagger UI e documentação
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
