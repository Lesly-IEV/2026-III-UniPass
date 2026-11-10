from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bicicletas", "0002_alter_bicicleta_usuario"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bicicleta",
            options={
                "permissions": [
                    ("administrar_bicicletas", "Puede registrar y editar cualquier bicicleta"),
                    ("editar_propia_bicicleta", "Puede editar las características de su bicicleta"),
                    ("ver_codigo_qr", "Puede ver el código QR de su bicicleta"),
                ]
            },
        ),
    ]
