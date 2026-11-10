from django.contrib.auth.models import User
from django.db import models


class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    matricula = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        permissions = [
            ("gestionar_usuarios", "Puede registrar y eliminar alumnos y guardias"),
            ("editar_propio_perfil", "Puede editar su propio perfil"),
        ]

    def __str__(self):
        nombre = self.user.get_full_name() or self.user.username
        if self.matricula:
            return f"{nombre} ({self.matricula})"
        return nombre
