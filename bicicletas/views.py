from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from cuentas.permisos import (
    ADMINISTRAR_BICICLETAS,
    EDITAR_BICICLETA,
    ESCANEAR,
    GESTIONAR_USUARIOS,
    VER_QR,
    bicicletas_de,
    requiere,
    requiere_alguno,
)

from .forms import BicicletaForm, CaracteristicasBicicletaForm
from .models import Bicicleta


@login_required
def mis_bicicletas(request):
    if request.user.has_perm(ESCANEAR) and not request.user.has_perm(GESTIONAR_USUARIOS):
        return redirect("verificar_acceso")

    return render(
        request,
        "bicicletas/mis_bicicletas.html",
        {"bicicletas": bicicletas_de(request.user)},
    )


@requiere(ADMINISTRAR_BICICLETAS)
def registrar_bicicleta(request):
    form = BicicletaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        bicicleta = form.save(commit=False)
        bicicleta.usuario = form.cleaned_data["alumno"]
        bicicleta.save()
        messages.success(request, "Bicicleta registrada y ligada al alumno elegido.")
        return redirect("mis_bicicletas")

    return render(request, "bicicletas/registrar_bicicleta.html", {"form": form})


@requiere_alguno(ADMINISTRAR_BICICLETAS, EDITAR_BICICLETA)
def editar_bicicleta(request, pk):
    bicicleta = get_object_or_404(bicicletas_de(request.user), pk=pk)
    form = CaracteristicasBicicletaForm(
        request.POST or None,
        instance=bicicleta,
        incluir_folio=request.user.has_perm(ADMINISTRAR_BICICLETAS),
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Características actualizadas.")
        return redirect("mis_bicicletas")

    return render(
        request,
        "bicicletas/editar_bicicleta.html",
        {"form": form, "bicicleta": bicicleta},
    )


@requiere_alguno(VER_QR, ADMINISTRAR_BICICLETAS)
def ver_qr(request, pk):
    bicicleta = get_object_or_404(bicicletas_de(request.user), pk=pk)
    return render(request, "bicicletas/qr.html", {"bicicleta": bicicleta})


@requiere(ADMINISTRAR_BICICLETAS)
@require_POST
def eliminar_bicicleta(request, pk):
    bicicleta = get_object_or_404(Bicicleta, pk=pk)
    folio = bicicleta.numero_folio
    bicicleta.delete()
    messages.success(request, f"Se eliminó la bicicleta con folio {folio}.")
    return redirect("mis_bicicletas")
