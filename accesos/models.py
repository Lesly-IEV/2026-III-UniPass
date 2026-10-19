from django.db import models
from cuentas.models import UsuarioPerfil
from bicicletas.models import Bicicleta

class RegistroAcceso(models.Model):
    ACCIONES = (
        ('Entrada', 'Entrada'),
        ('Salida', 'Salida'),
    )
    usuario = models.ForeignKey(UsuarioPerfil, on_delete=models.CASCADE, related_name='registros_acceso')
    bicicleta = models.ForeignKey(Bicicleta, on_delete=models.CASCADE, related_name='registros_acceso')
    marca_tiempo = models.DateTimeField(auto_now_add=True)
    tipo_accion = models.CharField(max_length=10, choices=ACCIONES)
    estado_verificado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario} - {self.tipo_accion} - {self.marca_tiempo}"