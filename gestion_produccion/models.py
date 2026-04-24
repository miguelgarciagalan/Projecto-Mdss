import uuid
from django.db import models
from gestion_materia_prima.models import LoteMateriaPrima


class LoteProduccion(models.Model):
    ESTADOS = [
        ('ARMADO', 'En armado'),
        ('FINALIZADO', 'Finalizado'),
    ]

    codigo_seguimiento = models.CharField(max_length=20, unique=True, editable=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='ARMADO')

    lotes_materia_prima = models.ManyToManyField(
        LoteMateriaPrima,
        related_name='lotes_produccion',
        verbose_name='Lotes de materia prima'
    )

    def save(self, *args, **kwargs):
        if not self.codigo_seguimiento:
            self.codigo_seguimiento = f"PROD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    @property
    def peso_total_neto(self):
        return sum(lote.peso_neto for lote in self.lotes_materia_prima.all())

    def __str__(self):
        return f"Lote de producción {self.codigo_seguimiento}"


class ProductoFinal(models.Model):
    TIPOS = [
        ('ACEITE', 'Aceite'),
        ('ACEITUNA_MESA', 'Aceituna de mesa'),
    ]

    UNIDADES = [
        ('L', 'Litros'),
        ('KG', 'Kilogramos'),
        ('UD', 'Unidades'),
    ]

    lote_produccion = models.ForeignKey(
        LoteProduccion,
        on_delete=models.CASCADE,
        related_name='productos_finales'
    )
    codigo = models.CharField(max_length=24, unique=True, editable=False)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    nombre = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=5, choices=UNIDADES, default='L')
    descripcion = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = str(uuid.uuid4().int)[:24]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"