from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cuentas", "0004_permisos_sin_rol"),
    ]

    operations = [
        migrations.AddField(
            model_name="perfilusuario",
            name="modo_acceso",
            field=models.CharField(
                choices=[("cliente", "Cliente"), ("lectura", "Solo lectura")],
                default="cliente",
                max_length=20,
            ),
        ),
    ]
