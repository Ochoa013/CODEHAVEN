from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SolicitudContacto",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=80, verbose_name="nombre")),
                (
                    "empresa",
                    models.CharField(blank=True, max_length=120, verbose_name="empresa"),
                ),
                ("telefono", models.CharField(max_length=15, verbose_name="teléfono")),
                ("correo", models.EmailField(max_length=254, verbose_name="correo electrónico")),
                (
                    "tipo_proyecto",
                    models.CharField(
                        choices=[
                            ("pagina_web", "Página web"),
                            ("aplicacion_web", "Aplicación web"),
                            ("sistema_empresarial", "Sistema empresarial"),
                            ("aplicacion_movil", "Aplicación móvil"),
                            ("aplicacion_escritorio", "Aplicación de escritorio"),
                            ("automatizacion", "Automatización"),
                            ("mantenimiento", "Mantenimiento de sistema"),
                            ("otro", "Otro"),
                        ],
                        max_length=30,
                        verbose_name="tipo de proyecto",
                    ),
                ),
                (
                    "presupuesto",
                    models.CharField(
                        blank=True,
                        max_length=80,
                        verbose_name="presupuesto aproximado",
                    ),
                ),
                ("mensaje", models.TextField(verbose_name="descripción del proyecto")),
                ("fecha", models.DateTimeField(auto_now_add=True, verbose_name="fecha")),
                (
                    "estado",
                    models.CharField(
                        choices=[
                            ("nueva", "Nueva"),
                            ("contactada", "Contactada"),
                            ("en_conversacion", "En conversación"),
                            ("finalizada", "Finalizada"),
                        ],
                        default="nueva",
                        max_length=20,
                        verbose_name="estado",
                    ),
                ),
            ],
            options={
                "verbose_name": "solicitud de contacto",
                "verbose_name_plural": "solicitudes de contacto",
                "ordering": ("-fecha",),
            },
        )
    ]
