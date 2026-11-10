from cuentas.permisos import perfil_de


def perfil_usuario(request):
    user = getattr(request, "user", None)
    if user is None or not user.is_authenticated:
        return {"perfil": None, "etiqueta": ""}
    grupo = user.groups.order_by("name").only("name").first()
    return {
        "perfil": perfil_de(user),
        "etiqueta": grupo.name if grupo else "Sin grupo",
    }
