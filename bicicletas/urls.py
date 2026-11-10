from django.urls import path

from . import views

urlpatterns = [
    path("mis-bicicletas/", views.mis_bicicletas, name="mis_bicicletas"),
    path("registrar/", views.registrar_bicicleta, name="registrar_bicicleta"),
    path("<int:pk>/editar/", views.editar_bicicleta, name="editar_bicicleta"),
    path("<int:pk>/eliminar/", views.eliminar_bicicleta, name="eliminar_bicicleta"),
    path("<int:pk>/qr/", views.ver_qr, name="ver_qr"),
]
