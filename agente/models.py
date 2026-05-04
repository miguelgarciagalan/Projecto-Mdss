from django.db import models


class Conversacion(models.Model):
    iniciada = models.DateTimeField(auto_now_add=True)
    historial_pydantic = models.TextField(default='[]')

    class Meta:
        verbose_name_plural = 'Conversaciones'

    def __str__(self):
        return f"Conversacion {self.id} ({self.iniciada.strftime('%d/%m/%Y %H:%M')})"


class MensajeConversacion(models.Model):
    ROLES = [('user', 'Usuario'), ('agent', 'Agente')]

    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='mensajes')
    rol = models.CharField(max_length=10, choices=ROLES)
    contenido = models.TextField()
    tools_usadas = models.TextField(blank=True, default='')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"[{self.rol}] {self.contenido[:60]}"
