from django.contrib import admin

from .models import SolicitudCotizacion


@admin.register(SolicitudCotizacion)
class SolicitudCotizacionAdmin(admin.ModelAdmin):
    list_display = (
        "cliente",
        "proyecto",
        "telefono",
        "email",
        "fecha_solicitud",
        "estado",
    )
    list_filter = ("estado", "tipo_proyecto", "fecha_solicitud", "notificacion_estado")
    search_fields = ("nombre", "empresa", "telefono", "email", "descripcion")
    list_editable = ("estado",)
    date_hierarchy = "fecha_solicitud"
    ordering = ("-fecha_solicitud",)
    readonly_fields = (
        "fecha_solicitud",
        "notificacion_estado",
        "notificacion_enviada",
        "notificacion_referencia",
        "notificacion_detalle",
    )
    fieldsets = (
        (
            "Datos de contacto",
            {"fields": ("nombre", "empresa", "telefono", "email", "preferencia_contacto")},
        ),
        (
            "Proyecto",
            {"fields": ("tipo_proyecto", "presupuesto", "descripcion")},
        ),
        ("Seguimiento", {"fields": ("estado", "fecha_solicitud")}),
        (
            "Notificación",
            {
                "fields": (
                    "notificacion_estado",
                    "notificacion_enviada",
                    "notificacion_referencia",
                    "notificacion_detalle",
                )
            },
        ),
    )

    @admin.display(description="Cliente", ordering="nombre")
    def cliente(self, obj):
        return obj.nombre

    @admin.display(description="Proyecto", ordering="tipo_proyecto")
    def proyecto(self, obj):
        return obj.get_tipo_proyecto_display()
