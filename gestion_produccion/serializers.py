from rest_framework import serializers

from gestion_materia_prima.models import LoteMateriaPrima
from gestion_materia_prima.serializers import LoteMateriaPrimaListSerializer
from gestion_produccion.models import LoteProduccion, ProductoFinal


class ProductoFinalListSerializer(serializers.ModelSerializer):
    lote_produccion_codigo = serializers.CharField(source='lote_produccion.codigo_seguimiento', read_only=True)

    class Meta:
        model = ProductoFinal
        fields = (
            'id',
            'codigo',
            'nombre',
            'tipo',
            'cantidad',
            'unidad',
            'lote_produccion',
            'lote_produccion_codigo',
        )


class ProductoFinalDetailSerializer(serializers.ModelSerializer):
    lote_produccion = serializers.SerializerMethodField()

    class Meta:
        model = ProductoFinal
        fields = (
            'id',
            'codigo',
            'nombre',
            'tipo',
            'cantidad',
            'unidad',
            'descripcion',
            'lote_produccion',
        )

    def get_lote_produccion(self, obj):
        return {
            'id': obj.lote_produccion_id,
            'codigo_seguimiento': obj.lote_produccion.codigo_seguimiento,
            'estado': obj.lote_produccion.estado,
        }


class ProductoFinalWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoFinal
        fields = ('id', 'lote_produccion', 'tipo', 'nombre', 'cantidad', 'unidad', 'descripcion')


class LoteProduccionListSerializer(serializers.ModelSerializer):
    total_lotes_materia_prima = serializers.SerializerMethodField()
    total_productos_finales = serializers.SerializerMethodField()
    peso_total_neto = serializers.FloatField(read_only=True)

    class Meta:
        model = LoteProduccion
        fields = (
            'id',
            'codigo_seguimiento',
            'fecha_creacion',
            'estado',
            'total_lotes_materia_prima',
            'total_productos_finales',
            'peso_total_neto',
        )

    def get_total_lotes_materia_prima(self, obj):
        return obj.lotes_materia_prima.count()

    def get_total_productos_finales(self, obj):
        return obj.productos_finales.count()


class LoteProduccionDetailSerializer(serializers.ModelSerializer):
    lotes_materia_prima = LoteMateriaPrimaListSerializer(many=True, read_only=True)
    productos_finales = ProductoFinalListSerializer(many=True, read_only=True)
    peso_total_neto = serializers.FloatField(read_only=True)

    class Meta:
        model = LoteProduccion
        fields = (
            'id',
            'codigo_seguimiento',
            'fecha_creacion',
            'estado',
            'peso_total_neto',
            'lotes_materia_prima',
            'productos_finales',
        )


class LoteProduccionWriteSerializer(serializers.ModelSerializer):
    lotes_materia_prima = serializers.PrimaryKeyRelatedField(
        queryset=LoteMateriaPrima.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = LoteProduccion
        fields = ('id', 'estado', 'lotes_materia_prima')

    def create(self, validated_data):
        lotes_materia_prima = validated_data.pop('lotes_materia_prima', [])
        instance = super().create(validated_data)
        if lotes_materia_prima:
            instance.lotes_materia_prima.set(lotes_materia_prima)
            LoteMateriaPrima.objects.filter(id__in=[lote.id for lote in lotes_materia_prima]).update(estado='ASIGNADO')
        return instance

    def update(self, instance, validated_data):
        lotes_materia_prima = validated_data.pop('lotes_materia_prima', None)
        instance = super().update(instance, validated_data)
        if lotes_materia_prima is not None:
            instance.lotes_materia_prima.set(lotes_materia_prima)
            LoteMateriaPrima.objects.filter(id__in=[lote.id for lote in lotes_materia_prima]).update(estado='ASIGNADO')
        return instance
