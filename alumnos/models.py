from django.db import models
from django.contrib.auth.models import User

class Alumno(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    carrera = models.CharField(max_length=100)
    creado = models.DateTimeField(auto_now_add=True)
    calificacion = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)


    def __str__(self):
        return self.nombre
