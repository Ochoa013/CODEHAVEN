from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("contacto", "0001_initial")]

    operations = [
        migrations.RenameModel(
            old_name="SolicitudContacto",
            new_name="SolicitudCotizacion",
        ),
        migrations.RenameField(
            model_name="solicitudcotizacion",
            old_name="correo",
            new_name="email",
        ),
        migrations.RenameField(
            model_name="solicitudcotizacion",
            old_name="mensaje",
            new_name="descripcion",
        ),
        migrations.RenameField(
            model_name="solicitudcotizacion",
            old_name="fecha",
            new_name="fecha_solicitud",
        ),
        migrations.AlterField(
            model_name="solicitudcotizacion",
            name="fecha_solicitud",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="fecha de solicitud"
            ),
        ),
        migrations.AlterModelOptions(
            name="solicitudcotizacion",
            options={
                "ordering": ("-fecha_solicitud",),
                "verbose_name": "solicitud de cotización",
                "verbose_name_plural": "solicitudes de cotización",
            },
        ),
        migrations.AlterField(
            model_name="solicitudcotizacion",
            name="tipo_proyecto",
            field=models.CharField(
                choices=[
                    ("pagina_web", "Página web profesional"),
                    ("aplicacion_web", "Aplicación web"),
                    ("sistema_empresarial", "Sistema empresarial"),
                    ("aplicacion_movil", "Aplicación móvil"),
                    ("aplicacion_escritorio", "Aplicación de escritorio"),
                    ("tienda_online", "Tienda online"),
                    ("inventario", "Sistema de inventario"),
                    ("ventas", "Sistema de ventas"),
                    ("recursos_humanos", "Sistema de Recursos Humanos"),
                    ("automatizacion", "Automatización de procesos"),
                    ("base_datos", "Base de datos"),
                    ("mantenimiento", "Mantenimiento de software"),
                    ("integracion", "Integración de sistemas"),
                    ("otro", "Otro"),
                ],
                max_length=30,
                verbose_name="tipo de proyecto",
            ),
        ),
        migrations.AlterField(
            model_name="solicitudcotizacion",
            name="estado",
            field=models.CharField(
                choices=[
                    ("nueva", "Nueva"),
                    ("contactada", "Contactada"),
                    ("en_conversacion", "En conversación"),
                    ("cotizada", "Cotizada"),
                    ("aceptada", "Aceptada"),
                    ("finalizada", "Finalizada"),
                ],
                default="nueva",
                max_length=20,
                verbose_name="estado",
            ),
        ),
        migrations.AddField(
            model_name="solicitudcotizacion",
            name="preferencia_contacto",
            field=models.CharField(
                choices=[
                    ("whatsapp", "WhatsApp"),
                    ("email", "Correo electrónico"),
                    ("llamada", "Llamada telefónica"),
                ],
                default="whatsapp",
                max_length=12,
                verbose_name="preferencia de contacto",
            ),
        ),
        migrations.AddField(
            model_name="solicitudcotizacion",
            name="notificacion_estado",
            field=models.CharField(
                choices=[
                    ("pendiente", "Pendiente"),
                    ("enviada_resend", "Enviada por Resend"),
                    ("enviada_smtp", "Enviada por SMTP"),
                    ("sin_configurar", "Proveedor no configurado"),
                    ("fallida", "Fallida"),
                ],
                default="pendiente",
                editable=False,
                max_length=20,
                verbose_name="estado de notificación",
            ),
        ),
        migrations.AddField(
            model_name="solicitudcotizacion",
            name="notificacion_enviada",
            field=models.DateTimeField(
                blank=True,
                editable=False,
                null=True,
                verbose_name="notificación enviada",
            ),
        ),
        migrations.AddField(
            model_name="solicitudcotizacion",
            name="notificacion_referencia",
            field=models.CharField(
                blank=True,
                editable=False,
                max_length=120,
                verbose_name="referencia de notificación",
            ),
        ),
        migrations.AddField(
            model_name="solicitudcotizacion",
            name="notificacion_detalle",
            field=models.CharField(
                blank=True,
                editable=False,
                max_length=255,
                verbose_name="detalle de notificación",
            ),
        ),
    ]
