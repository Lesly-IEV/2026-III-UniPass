from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="login", permanent=False)),
    path("admin/", admin.site.urls),
    path("", include("cuentas.urls")),
    path("bicicletas/", include("bicicletas.urls")),
    path("accesos/", include("accesos.urls")),
]
