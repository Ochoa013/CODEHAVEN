from django.db import models


class SolicitudCotizacion(models.Model):
    class TipoProyecto(models.TextChoices):
        PAGINA_WEB = "pagina_web", "Página web profesional"
        APLICACION_WEB = "aplicacion_web", "Aplicación web"
        SISTEMA_EMPRESARIAL = "sistema_empresarial", "Sistema empresarial"
        APLICACION_MOVIL = "aplicacion_movil", "Aplicación móvil"
        APLICACION_ESCRITORIO = "aplicacion_escritorio", "Aplicación de escritorio"
        TIENDA_ONLINE = "tienda_online", "Tienda online"
        INVENTARIO = "inventario", "Sistema de inventario"
        VENTAS = "ventas", "Sistema de ventas"
        RECURSOS_HUMANOS = "recursos_humanos", "Sistema de Recursos Humanos"
        AUTOMATIZACION = "automatizacion", "Automatización de procesos"
        BASE_DATOS = "base_datos", "Base de datos"
        MANTENIMIENTO = "mantenimiento", "Mantenimiento de software"
        INTEGRACION = "integracion", "Integración de sistemas"
        OTRO = "otro", "Otro"

    class PreferenciaContacto(models.TextChoices):
        WHATSAPP = "whatsapp", "WhatsApp"
        EMAIL = "email", "Correo electrónico"
        LLAMADA = "llamada", "Llamada telefónica"

    class Estado(models.TextChoices):
        NUEVA = "nueva", "Nueva"
        CONTACTADA = "contactada", "Contactada"
        EN_CONVERSACION = "en_conversacion", "En conversación"
        COTIZADA = "cotizada", "Cotizada"
        ACEPTADA = "aceptada", "Aceptada"
        FINALIZADA = "finalizada", "Finalizada"

    class EstadoNotificacion(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        ENVIADA_SMTP = "enviada_smtp", "Enviada por SMTP"
        SIN_CONFIGURAR = "sin_configurar", "Proveedor no configurado"
        FALLIDA = "fallida", "Fallida"

    nombre = models.CharField("nombre", max_length=80)
    empresa = models.CharField("empresa", max_length=120, blank=True)
    telefono = models.CharField("teléfono", max_length=15)
    email = models.EmailField("correo electrónico")
    tipo_proyecto = models.CharField(
        "tipo de proyecto", max_length=30, choices=TipoProyecto.choices
    )
    presupuesto = models.CharField("presupuesto aproximado", max_length=80, blank=True)
    descripcion = models.TextField("descripción del proyecto")
    preferencia_contacto = models.CharField(
        "preferencia de contacto",
        max_length=12,
        choices=PreferenciaContacto.choices,
        default=PreferenciaContacto.WHATSAPP,
    )
    fecha_solicitud = models.DateTimeField("fecha de solicitud", auto_now_add=True)
    estado = models.CharField(
        "estado", max_length=20, choices=Estado.choices, default=Estado.NUEVA
    )
    notificacion_estado = models.CharField(
        "estado de notificación",
        max_length=20,
        choices=EstadoNotificacion.choices,
        default=EstadoNotificacion.PENDIENTE,
        editable=False,
    )
    notificacion_enviada = models.DateTimeField(
        "notificación enviada", null=True, blank=True, editable=False
    )
    notificacion_referencia = models.CharField(
        "referencia de notificación", max_length=120, blank=True, editable=False
    )
    notificacion_detalle = models.CharField(
        "detalle de notificación", max_length=255, blank=True, editable=False
    )

    class Meta:
        verbose_name = "solicitud de cotización"
        verbose_name_plural = "solicitudes de cotización"
        ordering = ("-fecha_solicitud",)

    def __str__(self):
        return f"{self.nombre} — {self.get_tipo_proyecto_display()}"
