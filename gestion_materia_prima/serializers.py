from rest_framework import serializers

from gestion_materia_prima.models import LoteMateriaPrima, ResultadoAnalisis
from gestion_usuarios.serializers import ProductorDetailSerializer, ProductorListSerializer


class ResultadoAnalisisListSerializer(serializers.ModelSerializer):
    lote_codigo = serializers.CharField(source='lote.codigo', read_only=True)

    class Meta:
        model = ResultadoAnalisis
        fields = ('id', 'lote', 'lote_codigo', 'tipo_analisis', 'fecha_hora')


class ResultadoAnalisisDetailSerializer(serializers.ModelSerializer):
    lote = serializers.SerializerMethodField()

    class Meta:
        model = ResultadoAnalisis
        fields = ('id', 'lote', 'tipo_analisis', 'fecha_hora')

    def get_lote(self, obj):
        return {
            'id': obj.lote_id,
            'codigo': obj.lote.codigo,
            'estado': obj.lote.estado,
        }


class ResultadoAnalisisWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoAnalisis
        fields = ('id', 'lote', 'tipo_analisis')

    def create(self, validated_data):
        instance = super().create(validated_data)
        if instance.lote.estado != 'ASIGNADO':
            instance.lote.estado = 'ANALIZADO'
            instance.lote.save(update_fields=['estado'])
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if instance.lote.estado != 'ASIGNADO':
            instance.lote.estado = 'ANALIZADO'
            instance.lote.save(update_fields=['estado'])
        return instance


class LoteMateriaPrimaListSerializer(serializers.ModelSerializer):
    productor_nombre = serializers.SerializerMethodField()
    peso_neto = serializers.FloatField(read_only=True)

    class Meta:
        model = LoteMateriaPrima
        fields = (
            'id',
            'codigo',
            'productor',
            'productor_nombre',
            'fecha_cosecha',
            'fecha_arribo',
            'peso_bruto',
            'peso_tara',
            'peso_neto',
            'estado',
        )

    def get_productor_nombre(self, obj):
        return f'{obj.productor.nombre} {obj.productor.apellidos}'


class LoteMateriaPrimaDetailSerializer(serializers.ModelSerializer):
    productor = ProductorDetailSerializer(read_only=True)
    analisis = ResultadoAnalisisListSerializer(many=True, read_only=True)
    peso_neto = serializers.FloatField(read_only=True)
    lotes_produccion = serializers.SerializerMethodField()

    class Meta:
        model = LoteMateriaPrima
        fields = (
            'id',
            'codigo',
            'productor',
            'fecha_cosecha',
            'fecha_arribo',
            'peso_bruto',
            'peso_tara',
            'peso_neto',
            'estado',
            'analisis',
            'lotes_produccion',
        )

    def get_lotes_produccion(self, obj):
        return [
            {
                'id': lote.id,
                'codigo_seguimiento': lote.codigo_seguimiento,
                'estado': lote.estado,
            }
            for lote in obj.lotes_produccion.all()
        ]


class LoteMateriaPrimaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoteMateriaPrima
        fields = (
            'id',
            'productor',
            'fecha_cosecha',
            'peso_bruto',
            'peso_tara',
            'estado',
        )

