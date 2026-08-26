from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contacto", "0003_alter_solicitudcotizacion_notificacion_estado"),
    ]

    operations = [
        migrations.AlterField(
            model_name="solicitudcotizacion",
            name="notificacion_estado",
            field=models.CharField(
                choices=[
                    ("pendiente", "Pendiente"),
                    ("enviada_resend", "Enviada por Resend"),
                    ("enviada_smtp", "Enviada por SMTP (histórico)"),
                    ("sin_configurar", "Proveedor no configurado"),
                    ("fallida", "Fallida"),
                ],
                default="pendiente",
                editable=False,
                max_length=20,
                verbose_name="estado de notificación",
            ),
        ),
    ]
