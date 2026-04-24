from django.shortcuts import render

from gestion_usuarios.models import Productor
from gestion_materia_prima.models import LoteMateriaPrima
from gestion_produccion.models import LoteProduccion, ProductoFinal


def dashboard(request):
    context = {
        'total_productores': Productor.objects.count(),
        'total_lotes_mp': LoteMateriaPrima.objects.count(),
        'lotes_mp_ingresados': LoteMateriaPrima.objects.filter(estado='INGRESADO').count(),
        'lotes_mp_analizados': LoteMateriaPrima.objects.filter(estado='ANALIZADO').count(),
        'lotes_mp_asignados': LoteMateriaPrima.objects.filter(estado='ASIGNADO').count(),
        'total_lotes_produccion': LoteProduccion.objects.count(),
        'lotes_produccion_armado': LoteProduccion.objects.filter(estado='ARMADO').count(),
        'lotes_produccion_finalizado': LoteProduccion.objects.filter(estado='FINALIZADO').count(),
        'total_productos_finales': ProductoFinal.objects.count(),
    }
    return render(request, 'dashboard.html', context)
