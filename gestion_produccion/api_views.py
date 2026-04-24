from rest_framework import viewsets

from gestion_produccion.models import LoteProduccion, ProductoFinal
from gestion_produccion.serializers import (
    LoteProduccionDetailSerializer,
    LoteProduccionListSerializer,
    LoteProduccionWriteSerializer,
    ProductoFinalDetailSerializer,
    ProductoFinalListSerializer,
    ProductoFinalWriteSerializer,
)


class LoteProduccionViewSet(viewsets.ModelViewSet):
    queryset = LoteProduccion.objects.prefetch_related('lotes_materia_prima', 'productos_finales').order_by('-fecha_creacion')
    http_method_names = ['get', 'post', 'patch', 'head', 'options']
    filterset_fields = ('estado', 'fecha_creacion', 'codigo_seguimiento')
    search_fields = ('codigo_seguimiento',)
    ordering_fields = ('fecha_creacion', 'codigo_seguimiento', 'estado')

    def get_serializer_class(self):
        if self.action == 'list':
            return LoteProduccionListSerializer
        if self.action in ('create', 'partial_update'):
            return LoteProduccionWriteSerializer
        return LoteProduccionDetailSerializer


class ProductoFinalViewSet(viewsets.ModelViewSet):
    queryset = ProductoFinal.objects.select_related('lote_produccion').order_by('nombre', 'codigo')
    http_method_names = ['get', 'post', 'patch', 'head', 'options']
    filterset_fields = ('tipo', 'lote_produccion', 'codigo')
    search_fields = ('codigo', 'nombre', 'descripcion')
    ordering_fields = ('nombre', 'cantidad', 'codigo')

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductoFinalListSerializer
        if self.action in ('create', 'partial_update'):
            return ProductoFinalWriteSerializer
        return ProductoFinalDetailSerializer
