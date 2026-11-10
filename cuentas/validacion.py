import re

from django.core.exceptions import ValidationError

_NOMBRE = re.compile(
    r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]+(?:[ \-][A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]+)*$"
)
_USUARIO = re.compile(r"^[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*$")
_FOLIO = re.compile(r"^[A-Za-z0-9-]{1,50}$")
_CORREO = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")
_CLAVE_PROHIBIDA = re.compile(r"[<>\"'&;`]")

MENSAJE_TEXTO = "Solo se permiten letras, números, espacios y guiones."
MENSAJE_USUARIO = "El usuario solo puede tener letras, números y guiones."
MENSAJE_FOLIO = "El folio solo puede tener letras, números y guiones."
MENSAJE_CORREO = "El correo contiene caracteres no permitidos."
MENSAJE_CLAVE = "La contraseña no puede incluir estos caracteres: < > \" ' & ; `"


def texto_seguro(valor, mensaje=MENSAJE_TEXTO, vacio=False):
    texto = (valor or "").strip()
    if not texto and vacio:
        return ""
    if not texto or not _NOMBRE.fullmatch(texto):
        raise ValidationError(mensaje)
    return texto


def usuario_seguro(valor):
    texto = (valor or "").strip()
    if not _USUARIO.fullmatch(texto):
        raise ValidationError(MENSAJE_USUARIO)
    return texto


def folio_seguro(valor, mensaje=MENSAJE_FOLIO):
    texto = (valor or "").strip()
    if not _FOLIO.fullmatch(texto):
        raise ValidationError(mensaje)
    return texto


def correo_seguro(valor, vacio=False):
    texto = (valor or "").strip()
    if not texto and vacio:
        return ""
    if not _CORREO.fullmatch(texto):
        raise ValidationError(MENSAJE_CORREO)
    return texto


def clave_segura(valor, vacio=False):
    texto = valor or ""
    if not texto and vacio:
        return ""
    if _CLAVE_PROHIBIDA.search(texto):
        raise ValidationError(MENSAJE_CLAVE)
    return texto
