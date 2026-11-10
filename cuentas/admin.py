from django.contrib import admin

from .models import PerfilUsuario


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("user", "matricula")
    search_fields = ("user__username", "matricula", "user__first_name", "user__last_name")
