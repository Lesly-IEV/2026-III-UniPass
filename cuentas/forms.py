from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from cuentas.permisos import ALUMNO, GUARDIA


class NuevoUsuarioForm(forms.ModelForm):
    matricula = forms.CharField(
        label="Matrícula",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    tipo = forms.ChoiceField(
        label="Grupo",
        choices=[(ALUMNO, "Alumnos"), (GUARDIA, "Seguridad")],
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        labels = {
            "username": "Usuario",
            "first_name": "Nombre(s)",
            "last_name": "Apellidos",
            "email": "Correo",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. 20261234"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = False

    def clean(self):
        limpio = super().clean()
        if limpio.get("tipo") == ALUMNO and not (limpio.get("matricula") or "").strip():
            self.add_error("matricula", "La matrícula es obligatoria para un alumno.")
        return limpio


class PerfilForm(forms.Form):
    first_name = forms.CharField(label="Nombre(s)", max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Apellidos", max_length=150, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Correo", required=False, widget=forms.EmailInput(attrs={"class": "form-control"}))
    matricula = forms.CharField(label="Matrícula", max_length=20, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label="Nueva contraseña", required=False, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Confirmar contraseña", required=False, widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def __init__(self, *args, user=None, puede_editar_matricula=False, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        if not puede_editar_matricula:
            self.fields["matricula"].disabled = True
            self.fields["matricula"].help_text = "Solo un administrador puede cambiar la matrícula."

    def clean(self):
        limpio = super().clean()
        clave = limpio.get("password1") or ""
        confirmacion = limpio.get("password2") or ""
        if clave or confirmacion:
            if clave != confirmacion:
                self.add_error("password2", "Las contraseñas no coinciden.")
            else:
                try:
                    validate_password(clave, self.user)
                except ValidationError as exc:
                    self.add_error("password1", exc)
        return limpio
