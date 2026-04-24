from django.shortcuts import render, get_object_or_404
from .models import LoteProduccion


def lista_produccion(request):
    lotes_produccion = (
        LoteProduccion.objects
        .prefetch_related('lotes_materia_prima', 'productos_finales')
        .order_by('-fecha_creacion')
    )

    return render(
        request,
        'gestion_produccion/lista_produccion.html',
        {'lotes': lotes_produccion}
    )


def detalle_produccion(request, produccion_id):
    lote_p = get_object_or_404(
        LoteProduccion.objects.prefetch_related(
            'lotes_materia_prima__productor',
            'productos_finales'
        ),
        pk=produccion_id
    )

    return render(
        request,
        'gestion_produccion/detalle_produccion.html',
        {'lote_p': lote_p}
    )