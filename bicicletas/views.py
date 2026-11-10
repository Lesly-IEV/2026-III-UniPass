from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cuentas.models import PerfilUsuario
from .forms import BicicletaForm, RegistroAlumnoForm
from .models import Bicicleta

@login_required
def mis_bicicletas(request):
    perfil = getattr(request.user, 'perfilusuario', None) or getattr(request.user, 'perfil', None)
    bicicletas = Bicicleta.objects.filter(usuario=perfil) if perfil else []
    return render(request, 'bicicletas/mis_bicicletas.html', {'bicicletas': bicicletas})
@login_required
def registrar_bicicleta(request):
    perfil = getattr(request.user, 'perfilusuario', None) or getattr(request.user, 'perfil', None)
    rol_usuario = getattr(perfil, 'rol', '').lower() if perfil else ''

    if rol_usuario not in ['admin', 'administrativo']:
        messages.error(request, 'No tienes permisos para esta sección.')
        return redirect('mis_bicicletas')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'registrar_alumno':
            alumno_form = RegistroAlumnoForm(request.POST)
            bici_form = BicicletaForm()
            if alumno_form.is_valid():
                user = alumno_form.save(commit=False)
                user.set_password('UTVAM2026!')
                user.save()

                # Cambiado 'usuario=user' por 'user=user'
                PerfilUsuario.objects.get_or_create(
                    user=user,
                    defaults={'rol': 'alumno'}
                )
                messages.success(request, f'Alumno {user.username} registrado correctamente.')
                return redirect('registrar_bicicleta')

        elif action == 'registrar_bicicleta':
            bici_form = BicicletaForm(request.POST, request.FILES)
            alumno_form = RegistroAlumnoForm()
            if bici_form.is_valid():
                bicicleta = bici_form.save(commit=False)
                # Cambiado 'usuario=request.user' por 'user=request.user'
                perfil_actual, _ = PerfilUsuario.objects.get_or_create(user=request.user)
                bicicleta.usuario = perfil_actual
                bicicleta.save()
                messages.success(request, 'Bicicleta registrada correctamente.')
                return redirect('mis_bicicletas')
        else:
            bici_form = BicicletaForm()
            alumno_form = RegistroAlumnoForm()
    else:
        bici_form = BicicletaForm()
        alumno_form = RegistroAlumnoForm()

    return render(request, 'bicicletas/registrar_bicicleta.html', {
        'bici_form': bici_form,
        'alumno_form': alumno_form,
    })