from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from core.views import dashboard

schema_view = get_schema_view(
    openapi.Info(
        title='API Cooperativa Olivicola',
        default_version='v1',
        description='Documentacion de la API REST del proyecto final MDSS.',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('materia-prima/', include('gestion_materia_prima.urls')),
    path('produccion/', include('gestion_produccion.urls')),
    path('api/', include('core.api_urls')),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
