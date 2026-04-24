import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction

from gestion_usuarios.models import Productor
from gestion_materia_prima.models import LoteMateriaPrima, ResultadoAnalisis
from gestion_produccion.models import LoteProduccion, ProductoFinal


class Command(BaseCommand):
    help = 'Popula la base de datos con datos de prueba iniciales'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Populando base de datos...'))

        if LoteProduccion.objects.exists() and ProductoFinal.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    'Ya existen datos de ejemplo de produccion y productos finales. '
                    'No se duplicaron registros.'
                )
            )
            return

        with transaction.atomic():
            productores = [
                {
                    'nif': '12345678Z',
                    'nombre': 'Juan',
                    'apellidos': 'Perez Garcia',
                    'direccion': 'Calle del Olivo 5, Jaen',
                    'telefono': '600123456',
                    'email': 'juan@ejemplo.com',
                },
                {
                    'nif': '23456789D',
                    'nombre': 'Maria',
                    'apellidos': 'Lopez Romero',
                    'direccion': 'Avenida de la Cooperativa 12, Cordoba',
                    'telefono': '611234567',
                    'email': 'maria@ejemplo.com',
                },
            ]

            productores_creados = []
            for datos_productor in productores:
                productor, _ = Productor.objects.get_or_create(
                    nif=datos_productor['nif'],
                    defaults=datos_productor,
                )
                productores_creados.append(productor)

            lotes_creados = []
            tipos_analisis = ['Calidad inicial', 'Humedad', 'Madurez']

            for i in range(4):
                productor = productores_creados[i % len(productores_creados)]
                lote = LoteMateriaPrima.objects.create(
                    productor=productor,
                    fecha_cosecha=timezone.now().date(),
                    peso_bruto=2000.0 + (i * 175),
                    peso_tara=500.0 + (i * 15),
                    estado='ANALIZADO',
                )
                ResultadoAnalisis.objects.create(
                    lote=lote,
                    tipo_analisis=random.choice(tipos_analisis),
                )
                lotes_creados.append(lote)

            lote_produccion = LoteProduccion.objects.create(estado='ARMADO')
            lote_produccion.lotes_materia_prima.set(lotes_creados[:3])
            LoteMateriaPrima.objects.filter(id__in=[lote.id for lote in lotes_creados[:3]]).update(estado='ASIGNADO')

            ProductoFinal.objects.create(
                lote_produccion=lote_produccion,
                tipo='ACEITE',
                nombre='Aceite Virgen Extra',
                cantidad=Decimal('1500.00'),
                unidad='L',
                descripcion='Producto final principal obtenido del lote de produccion.',
            )

            ProductoFinal.objects.create(
                lote_produccion=lote_produccion,
                tipo='ACEITUNA_MESA',
                nombre='Aceituna de Mesa Seleccion',
                cantidad=Decimal('300.00'),
                unidad='KG',
                descripcion='Producto final secundario destinado a comercializacion.',
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Se crearon {len(productores_creados)} productores, '
                f'{len(lotes_creados)} lotes de materia prima, '
                f'{ResultadoAnalisis.objects.count()} resultados de analisis, '
                f'1 lote de produccion y '
                f'{ProductoFinal.objects.count()} productos finales.'
            )
        )
