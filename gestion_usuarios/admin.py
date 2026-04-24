from django.contrib import admin
from .models import Productor


@admin.register(Productor)
class ProductorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'nif', 'telefono', 'email')
    search_fields = ('nombre', 'apellidos', 'nif')
