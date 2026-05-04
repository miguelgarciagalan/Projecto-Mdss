from django.contrib import admin
from .models import Conversacion, MensajeConversacion


class MensajeInline(admin.TabularInline):
    model = MensajeConversacion
    extra = 0
    readonly_fields = ('rol', 'contenido', 'tools_usadas', 'timestamp')


@admin.register(Conversacion)
class ConversacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'iniciada')
    inlines = [MensajeInline]


@admin.register(MensajeConversacion)
class MensajeConversacionAdmin(admin.ModelAdmin):
    list_display = ('conversacion', 'rol', 'contenido', 'tools_usadas', 'timestamp')
    list_filter = ('rol',)
