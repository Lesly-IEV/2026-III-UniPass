from django.apps import AppConfig


class CuentasConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cuentas"

    def ready(self):
        from django.db.models.signals import post_migrate

        from cuentas.permisos import sincronizar_grupos

        post_migrate.connect(sincronizar_grupos, dispatch_uid="cuentas.sincronizar_grupos")
