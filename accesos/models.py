from django.db import models
from django.contrib.auth.models import User
from bicicletas.models import Bicicleta

class RegistroAcceso(models.Model):
    bicicleta = models.ForeignKey(Bicicleta, on_delete=models.CASCADE)
    tipo_acceso = models.CharField(max_length=10)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bicicleta} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"