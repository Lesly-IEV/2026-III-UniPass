from cuentas.permisos import es_solo_lectura, perfil_de


def perfil_usuario(request):
    user = getattr(request, "user", None)
    if user is None or not user.is_authenticated:
        return {"perfil": None, "etiqueta": "", "solo_lectura": False}
    grupo = user.groups.order_by("name").only("name").first()
    etiqueta = grupo.name if grupo else "Sin grupo"
    lectura = es_solo_lectura(user)
    if lectura:
        etiqueta = f"{etiqueta} · Solo lectura"
    return {
        "perfil": perfil_de(user),
        "etiqueta": etiqueta,
        "solo_lectura": lectura,
    }
