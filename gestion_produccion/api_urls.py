from django.urls import path

from gestion_produccion.api_views import LoteProduccionViewSet, ProductoFinalViewSet

lote_list = LoteProduccionViewSet.as_view({'get': 'list', 'post': 'create'})
lote_detail = LoteProduccionViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'})
producto_list = ProductoFinalViewSet.as_view({'get': 'list', 'post': 'create'})
producto_detail = ProductoFinalViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'})

urlpatterns = [
    path('lotes-produccion/', lote_list, name='api-lotes-produccion-list'),
    path('lotes-produccion/<int:pk>/', lote_detail, name='api-lotes-produccion-detail'),
    path('productos-finales/', producto_list, name='api-productos-finales-list'),
    path('productos-finales/<int:pk>/', producto_detail, name='api-productos-finales-detail'),
]
