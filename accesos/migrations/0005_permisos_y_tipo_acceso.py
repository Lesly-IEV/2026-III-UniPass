import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accesos", "0004_remove_registroacceso_permitido_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="registroacceso",
            options={
                "ordering": ["-fecha_hora"],
                "permissions": [
                    ("escanear_acceso", "Puede escanear códigos QR y registrar entrada o salida"),
                    ("ver_historial", "Puede ver el historial de accesos"),
                ],
            },
        ),
        migrations.AlterField(
            model_name="registroacceso",
            name="bicicleta",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="accesos",
                to="bicicletas.bicicleta",
            ),
        ),
        migrations.AlterField(
            model_name="registroacceso",
            name="tipo_acceso",
            field=models.CharField(
                choices=[("ENTRADA", "Entrada"), ("SALIDA", "Salida")],
                max_length=10,
            ),
        ),
    ]
