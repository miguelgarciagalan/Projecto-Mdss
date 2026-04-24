from rest_framework import viewsets

from gestion_materia_prima.models import LoteMateriaPrima, ResultadoAnalisis
from gestion_materia_prima.serializers import (
    LoteMateriaPrimaDetailSerializer,
    LoteMateriaPrimaListSerializer,
    LoteMateriaPrimaWriteSerializer,
    ResultadoAnalisisDetailSerializer,
    ResultadoAnalisisListSerializer,
    ResultadoAnalisisWriteSerializer,
)


class LoteMateriaPrimaViewSet(viewsets.ModelViewSet):
    queryset = LoteMateriaPrima.objects.select_related('productor').order_by('-fecha_arribo')
    http_method_names = ['get', 'post', 'patch', 'head', 'options']
    filterset_fields = ('estado', 'productor', 'fecha_cosecha', 'codigo')
    search_fields = ('codigo', 'productor__nombre', 'productor__apellidos', 'productor__nif')
    ordering_fields = ('fecha_cosecha', 'fecha_arribo', 'codigo', 'estado')

    def get_serializer_class(self):
        if self.action == 'list':
            return LoteMateriaPrimaListSerializer
        if self.action in ('create', 'partial_update'):
            return LoteMateriaPrimaWriteSerializer
        return LoteMateriaPrimaDetailSerializer


class ResultadoAnalisisViewSet(viewsets.ModelViewSet):
    queryset = ResultadoAnalisis.objects.select_related('lote').order_by('-fecha_hora')
    http_method_names = ['get', 'post', 'patch', 'head', 'options']
    filterset_fields = ('lote', 'tipo_analisis')
    search_fields = ('tipo_analisis', 'lote__codigo')
    ordering_fields = ('fecha_hora', 'tipo_analisis')

    def get_serializer_class(self):
        if self.action == 'list':
            return ResultadoAnalisisListSerializer
        if self.action in ('create', 'partial_update'):
            return ResultadoAnalisisWriteSerializer
        return ResultadoAnalisisDetailSerializer
