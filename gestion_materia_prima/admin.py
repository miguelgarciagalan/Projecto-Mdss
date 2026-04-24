from django.contrib import admin
from .models import LoteMateriaPrima, ResultadoAnalisis


class ResultadoAnalisisInline(admin.TabularInline):
    model = ResultadoAnalisis
    extra = 0


@admin.register(LoteMateriaPrima)
class LoteMateriaPrimaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'productor', 'fecha_cosecha', 'estado')
    list_filter = ('estado',)
    search_fields = ('codigo', 'productor__nombre', 'productor__apellidos')
    readonly_fields = ('codigo',)
    inlines = [ResultadoAnalisisInline]


@admin.register(ResultadoAnalisis)
class ResultadoAnalisisAdmin(admin.ModelAdmin):
    list_display = ('lote', 'tipo_analisis', 'fecha_hora')
    search_fields = ('lote__codigo', 'tipo_analisis')
