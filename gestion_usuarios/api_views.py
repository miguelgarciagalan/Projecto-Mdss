from rest_framework import viewsets

from gestion_usuarios.models import Productor
from gestion_usuarios.serializers import (
    ProductorDetailSerializer,
    ProductorListSerializer,
    ProductorWriteSerializer,
)


class ProductorViewSet(viewsets.ModelViewSet):
    queryset = Productor.objects.all().order_by('nombre', 'apellidos')
    http_method_names = ['get', 'post', 'patch', 'head', 'options']
    filterset_fields = ('nif',)
    search_fields = ('nombre', 'apellidos', 'nif', 'email', 'telefono')
    ordering_fields = ('nombre', 'apellidos', 'nif', 'email')

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductorListSerializer
        if self.action in ('create', 'partial_update'):
            return ProductorWriteSerializer
        return ProductorDetailSerializer
