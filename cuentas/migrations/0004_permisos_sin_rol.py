from django.db import migrations, models


def asignar_grupos_desde_rol(apps, schema_editor):
    """Pasa el texto viejo de rol al grupo correspondiente y deja un solo grupo."""
    PerfilUsuario = apps.get_model("cuentas", "PerfilUsuario")
    Group = apps.get_model("auth", "Group")
    mapa = {
        "admin": "Administrador",
        "administrativo": "Administrador",
        "policia": "Guardia",
        "guardia": "Guardia",
        "alumno": "Alumno",
    }
    for perfil in PerfilUsuario.objects.all():
        nombre = mapa.get((perfil.rol or "").lower(), "Alumno")
        grupo, _ = Group.objects.get_or_create(name=nombre)
        perfil.user.groups.set([grupo])


class Migration(migrations.Migration):

    dependencies = [
        ("cuentas", "0003_delete_usuarioperfil"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(asignar_grupos_desde_rol, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="perfilusuario",
            name="rol",
        ),
        migrations.AlterModelOptions(
            name="perfilusuario",
            options={
                "permissions": [
                    ("gestionar_usuarios", "Puede registrar y eliminar alumnos y guardias"),
                    ("editar_propio_perfil", "Puede editar su propio perfil"),
                ]
            },
        ),
    ]
