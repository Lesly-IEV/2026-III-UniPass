from django.contrib import admin

from .models import RegistroAcceso


@admin.register(RegistroAcceso)
class RegistroAccesoAdmin(admin.ModelAdmin):
    list_display = ("bicicleta", "tipo_acceso", "registrado_por", "fecha_hora")
    list_filter = ("tipo_acceso",)
