from django import forms

from cuentas.models import PerfilUsuario
from cuentas.permisos import ALUMNO

from .models import Bicicleta


class BicicletaForm(forms.ModelForm):
    alumno = forms.ModelChoiceField(
        label="Alumno",
        queryset=PerfilUsuario.objects.none(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Bicicleta
        fields = ["numero_folio", "marca", "color"]
        widgets = {
            "numero_folio": forms.TextInput(attrs={"class": "form-control"}),
            "marca": forms.TextInput(attrs={"class": "form-control"}),
            "color": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["alumno"].queryset = (
            PerfilUsuario.objects.filter(user__groups__name=ALUMNO)
            .select_related("user")
            .order_by("user__first_name", "user__username")
        )


class CaracteristicasBicicletaForm(forms.ModelForm):
    class Meta:
        model = Bicicleta
        fields = ["numero_folio", "marca", "color"]
        widgets = {
            "numero_folio": forms.TextInput(attrs={"class": "form-control"}),
            "marca": forms.TextInput(attrs={"class": "form-control"}),
            "color": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, incluir_folio=False, **kwargs):
        super().__init__(*args, **kwargs)
        if not incluir_folio:
            self.fields.pop("numero_folio")
