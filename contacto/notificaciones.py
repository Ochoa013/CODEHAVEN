"""Notificaciones de nuevas cotizaciones mediante Gmail SMTP."""

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils import timezone

from .models import SolicitudCotizacion


class ProveedorNoConfigurado(Exception):
    pass


def _contenido_notificacion(cotizacion):
    context = {
        "cotizacion": cotizacion,
        "destinatario": settings.COTIZACIONES_EMAIL,
    }
    asunto = f"Nueva solicitud de cotización - {cotizacion.nombre}"
    html = render_to_string("emails/nueva_cotizacion.html", context)
    texto = render_to_string("emails/nueva_cotizacion.txt", context)
    return asunto, html, texto


def _enviar_smtp(cotizacion, asunto, html, texto):
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        raise ProveedorNoConfigurado("SMTP no está configurado")

    connection = get_connection(fail_silently=False)
    email = EmailMultiAlternatives(
        subject=asunto,
        body=texto,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.COTIZACIONES_EMAIL],
        reply_to=[cotizacion.email],
        connection=connection,
    )
    email.attach_alternative(html, "text/html")
    sent = email.send(fail_silently=False)
    if sent != 1:
        raise RuntimeError("SMTP no confirmó el envío")
    return "smtp"


def _registrar_resultado(cotizacion, estado, detalle="", referencia=""):
    sent_states = {SolicitudCotizacion.EstadoNotificacion.ENVIADA_SMTP}
    cotizacion.notificacion_estado = estado
    cotizacion.notificacion_detalle = detalle[:255]
    cotizacion.notificacion_referencia = referencia[:120]
    cotizacion.notificacion_enviada = timezone.now() if estado in sent_states else None
    cotizacion.save(
        update_fields=(
            "notificacion_estado",
            "notificacion_detalle",
            "notificacion_referencia",
            "notificacion_enviada",
        )
    )


def notificar_nueva_cotizacion(cotizacion):
    """Envía una sola notificación mediante SMTP sin interrumpir al visitante."""
    if cotizacion.notificacion_estado == SolicitudCotizacion.EstadoNotificacion.ENVIADA_SMTP:
        return cotizacion.notificacion_estado

    asunto, html, texto = _contenido_notificacion(cotizacion)
    smtp_configurado = bool(settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD)

    if not smtp_configurado:
        _registrar_resultado(
            cotizacion,
            SolicitudCotizacion.EstadoNotificacion.SIN_CONFIGURAR,
            "Configura EMAIL_HOST_USER y EMAIL_HOST_PASSWORD.",
        )
        return cotizacion.notificacion_estado

    try:
        reference = _enviar_smtp(cotizacion, asunto, html, texto)
        _registrar_resultado(
            cotizacion,
            SolicitudCotizacion.EstadoNotificacion.ENVIADA_SMTP,
            "Notificación entregada mediante Gmail SMTP.",
            reference,
        )
    except Exception as exc:  # El visitante nunca debe recibir un error del proveedor.
        _registrar_resultado(
            cotizacion,
            SolicitudCotizacion.EstadoNotificacion.FALLIDA,
            str(exc) or "El servidor SMTP no confirmó el envío.",
        )
    return cotizacion.notificacion_estado
