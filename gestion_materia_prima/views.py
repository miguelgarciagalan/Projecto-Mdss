from django.shortcuts import render, get_object_or_404
from .models import LoteMateriaPrima

def lista_lotes(request):
    lotes = (
        LoteMateriaPrima.objects.select_related('productor')
        .order_by('-fecha_arribo')
    )
    return render(request, 'gestion_materia_prima/lista_lotes.html', {'lotes': lotes})

def detalle_lote(request, lote_id):
    lote = get_object_or_404(
        LoteMateriaPrima.objects.select_related('productor').prefetch_related('analisis'),
        pk=lote_id,
    )
    return render(
        request,
        'gestion_materia_prima/detalle_lote.html',
        {
            'lote': lote,
            'analisis_list': lote.analisis.all(),
        },
    )
