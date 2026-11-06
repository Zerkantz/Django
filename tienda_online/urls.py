"""
URL configuration for tienda_online project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Configuración de Swagger y OpenAPI
schema_view = get_schema_view(
    openapi.Info(
        title="Tienda Online API",
        default_version='v1',
        description=(
            "API RESTful para el sistema de Tienda Online.\n\n"
            "Módulos incluidos:\n"
            "- Gestión de usuarios con modelo personalizado (autenticación por email y campo 'telefono').\n"
            "- Autenticación mediante JSON Web Tokens (JWT) con tiempo de vida configurado (ACCESS_TOKEN_LIFETIME).\n"
            "- Endpoints de datos personales del usuario logueado (/api/v1/auth/me/).\n"
            "- Catálogo de Categorías y Productos con cálculo de precios y filtros."
        ),
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contacto@tiendaonline.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),

    # Endpoints de la API v1 (Usuarios, Autenticación y Catálogo)
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('products.urls')),

    # Documentación interactiva Swagger y ReDoc
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
