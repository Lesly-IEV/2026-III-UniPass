from django.contrib.auth.models import User
from django.db import models

from bicicletas.models import Bicicleta


class RegistroAcceso(models.Model):
    ENTRADA = "ENTRADA"
    SALIDA = "SALIDA"
    TIPOS = [
        (ENTRADA, "Entrada"),
        (SALIDA, "Salida"),
    ]

    bicicleta = models.ForeignKey(Bicicleta, on_delete=models.CASCADE, related_name="accesos")
    tipo_acceso = models.CharField(max_length=10, choices=TIPOS)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_hora"]
        permissions = [
            ("escanear_acceso", "Puede escanear códigos QR y registrar entrada o salida"),
            ("ver_historial", "Puede ver el historial de accesos"),
        ]

    def __str__(self):
        return f"{self.bicicleta} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"
