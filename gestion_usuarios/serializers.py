from rest_framework import serializers

from gestion_usuarios.models import Productor


class ProductorListSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Productor
        fields = ('id', 'nombre_completo', 'nif', 'telefono', 'email')

    def get_nombre_completo(self, obj):
        return f'{obj.nombre} {obj.apellidos}'


class ProductorDetailSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Productor
        fields = (
            'id',
            'nombre',
            'apellidos',
            'nombre_completo',
            'nif',
            'direccion',
            'telefono',
            'email',
        )

    def get_nombre_completo(self, obj):
        return f'{obj.nombre} {obj.apellidos}'


class ProductorWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productor
        fields = ('id', 'nombre', 'apellidos', 'nif', 'direccion', 'telefono', 'email')
