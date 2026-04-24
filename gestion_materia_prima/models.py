import uuid
from django.db import models
from gestion_usuarios.models import Productor


class LoteMateriaPrima(models.Model):
    ESTADOS = [
        ('INGRESADO', 'Ingresado'),
        ('ANALISIS', 'En análisis'),
        ('ANALIZADO', 'Analizado'),
        ('ASIGNADO', 'Asignado a Lote de producción'),
    ]

    productor = models.ForeignKey(Productor, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=24, unique=True, editable=False)
    fecha_cosecha = models.DateField()
    fecha_arribo = models.DateTimeField(auto_now_add=True)
    peso_bruto = models.FloatField()
    peso_tara = models.FloatField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='INGRESADO')

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = str(uuid.uuid4().int)[:24]
        super().save(*args, **kwargs)

    @property
    def peso_neto(self):
        if self.peso_bruto is not None and self.peso_tara is not None:
            return self.peso_bruto - self.peso_tara
        return 0

    def __str__(self):
        return f"Lote {self.codigo} ({self.productor.nombre})"


class ResultadoAnalisis(models.Model):
    lote = models.ForeignKey(LoteMateriaPrima, on_delete=models.CASCADE, related_name='analisis')
    tipo_analisis = models.CharField(max_length=100)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analisis {self.tipo_analisis} - Lote {self.lote.codigo}"
