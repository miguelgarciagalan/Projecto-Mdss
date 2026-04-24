from django.db import models


class Productor(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    nif = models.CharField(max_length=9, unique=True, verbose_name="NIF/DNI")
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.nif})"

    class Meta:
        verbose_name_plural = "Productores"
