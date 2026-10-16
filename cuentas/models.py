from django.db import models
from django.contrib.auth.models import User

class UsuarioPerfil(models.Model):
    ROLES = (
        ('Admin', 'Admin'),
        ('Sistemas', 'Sistemas'),
        ('Policia', 'Policia'),
        ('Alumno', 'Alumno'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='Alumno')
    telefono = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"