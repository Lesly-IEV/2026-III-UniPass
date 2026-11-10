from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from bicicletas.models import Bicicleta
from .models import RegistroAcceso

@login_required
def historial_accesos(request):
    # Verificación de rol (Policía/Guardia/Admin)
    perfil = getattr(request.user, 'perfilusuario', None) or getattr(request.user, 'perfil', None)
    rol = getattr(perfil, 'rol', '').lower() if perfil else ''

    if rol not in ['policia', 'guardia', 'admin', 'administrativo']:
        messages.error(request, 'No tienes permiso para acceder a esta sección.')
        return redirect('mis_bicicletas')

    # Obtenemos todos los registros ordenados del más reciente al más antiguo
    registros = RegistroAcceso.objects.select_related(
        'bicicleta__usuario__user', 
        'registrado_por'
    ).order_by('-fecha_hora')

    return render(request, 'accesos/historial.html', {
        'registros': registros
    })
def verificar_acceso(request):
    perfil = getattr(request.user, 'perfilusuario', None) or getattr(request.user, 'perfil', None)
    rol = getattr(perfil, 'rol', '').lower() if perfil else ''

    if rol not in ['policia', 'guardia', 'admin', 'administrativo']:
        messages.error(request, 'No tienes permiso para acceder a esta sección.')
        return redirect('mis_bicicletas')

    bicicleta = None
    query = ''

    if request.method == 'POST':
        action = request.POST.get('action')
        query = (request.POST.get('codigo') or request.POST.get('folio') or '').strip()

        # Búsqueda de la bicicleta
        if query:
            bicicleta = Bicicleta.objects.filter(numero_folio=query).select_related('usuario__user').first()
            if not bicicleta and hasattr(Bicicleta, 'folio'):
                bicicleta = Bicicleta.objects.filter(folio=query).select_related('usuario__user').first()

        # Registro de Entrada / Salida
        if action in ['registrar_entrada', 'registrar_salida']:
            bici_id = request.POST.get('bicicleta_id')
            if bici_id:
                bici_obj = Bicicleta.objects.filter(id=bici_id).first()
                tipo_movimiento = 'ENTRADA' if action == 'registrar_entrada' else 'SALIDA'

                if bici_obj:
                    RegistroAcceso.objects.create(
                        bicicleta=bici_obj,
                        tipo_acceso=tipo_movimiento,
                        registrado_por=request.user
                    )
                    messages.success(
                        request, 
                        f'✅ {tipo_movimiento.capitalize()} registrada correctamente.'
                    )
                    return redirect('verificar_acceso')

        elif not bicicleta and query:
            messages.error(request, f"No se encontró ninguna bicicleta registrada con el folio '{query}'.")

    return render(request, 'accesos/verificar.html', {
        'bicicleta': bicicleta,
        'query': query,
    })