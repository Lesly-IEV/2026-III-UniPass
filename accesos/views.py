import uuid

from django.contrib import messages
from django.shortcuts import redirect, render

from bicicletas.models import Bicicleta
from cuentas.permisos import ESCANEAR, VER_HISTORIAL, requiere

from .models import RegistroAcceso


def _buscar_por_token(valor):
    texto = (valor or "").strip()
    if not texto:
        return None
    try:
        token = uuid.UUID(texto)
    except ValueError:
        return None
    return Bicicleta.objects.filter(qr_token=token).select_related("usuario__user").first()


@requiere(VER_HISTORIAL)
def historial_accesos(request):
    registros = RegistroAcceso.objects.select_related(
        "bicicleta__usuario__user",
        "registrado_por",
    )
    return render(request, "accesos/historial.html", {"registros": registros})


@requiere(ESCANEAR)
def verificar_acceso(request):
    bicicleta = None
    query = ""

    if request.method == "POST":
        accion = request.POST.get("action")
        query = (request.POST.get("codigo") or request.POST.get("qr_token") or "").strip()[:80]

        if accion in ("registrar_entrada", "registrar_salida"):
            bicicleta = _buscar_por_token(request.POST.get("qr_token"))
            if bicicleta is None:
                messages.error(request, "El código QR no corresponde a una bicicleta registrada.")
            else:
                _registrar_movimiento(request, bicicleta, accion)
            return redirect("verificar_acceso")
        else:
            bicicleta = _buscar_por_token(query)
            if bicicleta is None:
                messages.error(request, "No se encontró una bicicleta con ese código QR.")

    return render(
        request,
        "accesos/verificar.html",
        {"bicicleta": bicicleta, "query": query},
    )


def _registrar_movimiento(request, bicicleta, accion):
    ultimo = bicicleta.accesos.order_by("-fecha_hora").first()
    if accion == "registrar_entrada":
        if ultimo and ultimo.tipo_acceso == RegistroAcceso.ENTRADA:
            messages.error(request, "Esa bicicleta ya tiene una entrada abierta.")
            return
        tipo = RegistroAcceso.ENTRADA
    else:
        if ultimo is None or ultimo.tipo_acceso != RegistroAcceso.ENTRADA:
            messages.error(request, "No hay una entrada abierta para registrar la salida.")
            return
        tipo = RegistroAcceso.SALIDA

    RegistroAcceso.objects.create(
        bicicleta=bicicleta,
        tipo_acceso=tipo,
        registrado_por=request.user,
    )
    messages.success(request, f"{tipo.capitalize()} registrada.")
