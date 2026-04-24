from django.contrib import admin
from .models import LoteProduccion, ProductoFinal


class ProductoFinalInline(admin.TabularInline):
    model = ProductoFinal
    extra = 1


@admin.register(LoteProduccion)
class LoteProduccionAdmin(admin.ModelAdmin):
    list_display = ('codigo_seguimiento', 'estado', 'fecha_creacion')
    list_filter = ('estado',)
    search_fields = ('codigo_seguimiento',)
    filter_horizontal = ('lotes_materia_prima',)
    inlines = [ProductoFinalInline]


@admin.register(ProductoFinal)
class ProductoFinalAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'tipo', 'cantidad', 'unidad', 'lote_produccion')
    list_filter = ('tipo',)
    search_fields = ('codigo', 'nombre')
