from django.urls import path
from . import views

urlpatterns = [
    path('verificar/', views.verificar_acceso, name='verificar_acceso'),
    path('historial/', views.historial_accesos, name='historial_accesos'),
]