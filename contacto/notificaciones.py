"""Notificaciones de nuevas cotizaciones mediante Resend."""

import logging

import resend
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone

from .models import SolicitudCotizacion


logger = logging.getLogger(__name__)


class ProveedorNoConfigurado(Exception):
    pass


def _contenido_notificacion(cotizacion):
    context = {"cotizacion": cotizacion}
    asunto = f"Nueva solicitud de desarrollo de software - {cotizacion.nombre}"
    html = render_to_string("emails/nueva_cotizacion.html", context)
    texto = render_to_string("emails/nueva_cotizacion.txt", context)
    return asunto, html, texto


def _resend_configurado():
    return bool(
        settings.RESEND_API_KEY
        and settings.RESEND_FROM_EMAIL
        and settings.CONTACT_EMAIL
    )


def _enviar_resend(cotizacion, asunto, html, texto):
    if not _resend_configurado():
        raise ProveedorNoConfigurado("Resend no está configurado")

    resend.api_key = settings.RESEND_API_KEY
    params: resend.Emails.SendParams = {
        "from": f"CODEHAVEN <{settings.RESEND_FROM_EMAIL}>",
        "to": [settings.CONTACT_EMAIL],
        "reply_to": cotizacion.email,
        "subject": asunto,
        "html": html,
        "text": texto,
    }
    response = resend.Emails.send(
        params,
        {"idempotency_key": f"cotizacion-{cotizacion.pk}"},
    )
    reference = response.get("id") if response else None
    if not reference:
        raise RuntimeError("Resend no confirmó el envío")
    return reference


def _registrar_resultado(cotizacion, estado, detalle="", referencia=""):
    sent_states = {SolicitudCotizacion.EstadoNotificacion.ENVIADA_RESEND}
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
    """Envía una sola notificación mediante Resend sin exponer fallos al visitante."""
    if cotizacion.notificacion_estado == SolicitudCotizacion.EstadoNotificacion.ENVIADA_RESEND:
        return cotizacion.notificacion_estado

    asunto, html, texto = _contenido_notificacion(cotizacion)

    if not _resend_configurado():
        _registrar_resultado(
            cotizacion,
            SolicitudCotizacion.EstadoNotificacion.SIN_CONFIGURAR,
            "Configura las credenciales y direcciones de Resend.",
        )
        return cotizacion.notificacion_estado

    try:
        reference = _enviar_resend(cotizacion, asunto, html, texto)
        _registrar_resultado(
            cotizacion,
            SolicitudCotizacion.EstadoNotificacion.ENVIADA_RESEND,
            "Notificación aceptada por Resend.",
            reference,
        )
    except Exception:  # El visitante nunca debe recibir detalles del proveedor.
        logger.exception("Error enviando solicitud de cotización mediante Resend")
        _registrar_resultado(
            cotizacion,
            SolicitudCotizacion.EstadoNotificacion.FALLIDA,
            "Resend no confirmó el envío.",
        )
    return cotizacion.notificacion_estado
