from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from gestion_usuarios.api_views import ProductorViewSet
from gestion_materia_prima.api_views import LoteMateriaPrimaViewSet, ResultadoAnalisisViewSet
from gestion_produccion.api_views import LoteProduccionViewSet, ProductoFinalViewSet

router = DefaultRouter()
router.register(r'productores', ProductorViewSet, basename='productores')
router.register(r'lotes-materia-prima', LoteMateriaPrimaViewSet, basename='lotes-materia-prima')
router.register(r'resultados-analisis', ResultadoAnalisisViewSet, basename='resultados-analisis')
router.register(r'lotes-produccion', LoteProduccionViewSet, basename='lotes-produccion')
router.register(r'productos-finales', ProductoFinalViewSet, basename='productos-finales')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
