from django.db import models

class Reporte(models.Model):
    nombre = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha = models.DateField()

    def __str__(self):
        return f"{self.nombre} ({self.fecha})"
