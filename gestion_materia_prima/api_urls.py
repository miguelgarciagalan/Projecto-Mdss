from django.urls import path

from gestion_materia_prima.api_views import LoteMateriaPrimaViewSet, ResultadoAnalisisViewSet

lote_list = LoteMateriaPrimaViewSet.as_view({'get': 'list', 'post': 'create'})
lote_detail = LoteMateriaPrimaViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'})
analisis_list = ResultadoAnalisisViewSet.as_view({'get': 'list', 'post': 'create'})
analisis_detail = ResultadoAnalisisViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'})

urlpatterns = [
    path('lotes-materia-prima/', lote_list, name='api-lotes-materia-prima-list'),
    path('lotes-materia-prima/<int:pk>/', lote_detail, name='api-lotes-materia-prima-detail'),
    path('resultados-analisis/', analisis_list, name='api-resultados-analisis-list'),
    path('resultados-analisis/<int:pk>/', analisis_detail, name='api-resultados-analisis-detail'),
]
