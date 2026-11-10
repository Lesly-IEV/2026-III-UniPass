import uuid

from django.db import models


class Bicicleta(models.Model):
    usuario = models.ForeignKey(
        "cuentas.PerfilUsuario",
        on_delete=models.CASCADE,
        related_name="bicicletas",
    )
    numero_folio = models.CharField(max_length=50, unique=True)
    marca = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    qr_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        permissions = [
            ("administrar_bicicletas", "Puede registrar y editar cualquier bicicleta"),
            ("editar_propia_bicicleta", "Puede editar las características de su bicicleta"),
            ("ver_codigo_qr", "Puede ver el código QR de su bicicleta"),
        ]

    def __str__(self):
        return f"{self.marca} ({self.numero_folio})"
