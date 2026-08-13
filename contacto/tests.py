import time
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.core import signing
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import SolicitudCotizacion
from .notificaciones import (
    _contenido_notificacion,
    _enviar_smtp,
    notificar_nueva_cotizacion,
)


class SitioTests(TestCase):
    def valid_payload(self, **changes):
        payload = {
            "nombre": "María José",
            "empresa": "Negocio Demo",
            "telefono": "0991234567",
            "email": "maria@example.com",
            "tipo_proyecto": "aplicacion_web",
            "presupuesto": "Por definir",
            "descripcion": "Necesito digitalizar el proceso de ventas de mi negocio.",
            "preferencia_contacto": "whatsapp",
            "website": "",
            "started_at": signing.dumps(time.time() - 3, salt="contact-form"),
        }
        payload.update(changes)
        return payload

    def test_home_carga_con_formulario_y_contenido_principal(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Convierte tu idea en")
        self.assertContains(response, "Solicitar cotización")
        self.assertContains(response, "CODEHAVEN")
        self.assertContains(response, "Carrusel de especialidades")
        self.assertNotContains(response, 'id="sobre-mi"')
        self.assertContains(response, "csrfmiddlewaretoken")

    @patch("contacto.views.notificar_nueva_cotizacion")
    def test_solicitud_valida_se_guarda_y_muestra_confirmacion(self, notify):
        response = self.client.post(reverse("solicitar_contacto"), self.valid_payload(), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SolicitudCotizacion.objects.count(), 1)
        notify.assert_called_once()
        self.assertContains(response, "¡Solicitud recibida!")
        self.assertContains(response, "acabo%20de%20enviar%20una%20solicitud")

    def test_validacion_servidor_rechaza_datos_invalidos(self):
        response = self.client.post(
            reverse("solicitar_contacto"),
            self.valid_payload(
                nombre="1234",
                telefono="teléfono",
                email="correo-invalido",
                descripcion="Muy corto",
            ),
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(SolicitudCotizacion.objects.count(), 0)
        self.assertContains(response, "Escribe un correo electrónico válido", status_code=422)

    def test_honeypot_rechaza_spam(self):
        response = self.client.post(
            reverse("solicitar_contacto"),
            self.valid_payload(website="https://spam.example"),
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(SolicitudCotizacion.objects.count(), 0)

    def test_nombre_con_numeros_es_rechazado(self):
        response = self.client.post(
            reverse("solicitar_contacto"), self.valid_payload(nombre="Juan123")
        )
        self.assertEqual(response.status_code, 422)
        self.assertContains(response, "El nombre solo puede contener letras", status_code=422)

    @override_settings(
        EMAIL_HOST_USER="ochoaesteban593@gmail.com",
        EMAIL_HOST_PASSWORD="app-password-test",
        COTIZACIONES_EMAIL="ochoaesteban593@gmail.com",
    )
    @patch("contacto.notificaciones._enviar_smtp", return_value="smtp")
    def test_smtp_es_el_unico_proveedor_y_registra_el_envio(self, smtp):
        cotizacion = SolicitudCotizacion.objects.create(
            nombre="Cliente de prueba",
            telefono="0999999999",
            email="cliente@example.com",
            tipo_proyecto="aplicacion_web",
            descripcion="Necesito desarrollar un sistema web para administrar mi negocio.",
            preferencia_contacto="llamada",
        )
        estado = notificar_nueva_cotizacion(cotizacion)
        cotizacion.refresh_from_db()
        self.assertEqual(estado, SolicitudCotizacion.EstadoNotificacion.ENVIADA_SMTP)
        self.assertEqual(cotizacion.notificacion_referencia, "smtp")
        smtp.assert_called_once()

    @override_settings(EMAIL_HOST_USER="", EMAIL_HOST_PASSWORD="")
    @patch("contacto.notificaciones._enviar_smtp")
    def test_smtp_sin_credenciales_no_intenta_enviar(self, smtp):
        cotizacion = SolicitudCotizacion.objects.create(
            nombre="Cliente sin configuración",
            telefono="0999999999",
            email="cliente@example.com",
            tipo_proyecto="aplicacion_web",
            descripcion="Necesito desarrollar una aplicación web para gestionar clientes.",
            preferencia_contacto="email",
        )
        estado = notificar_nueva_cotizacion(cotizacion)
        self.assertEqual(estado, SolicitudCotizacion.EstadoNotificacion.SIN_CONFIGURAR)
        smtp.assert_not_called()

    @override_settings(
        EMAIL_HOST_USER="ochoaesteban593@gmail.com",
        EMAIL_HOST_PASSWORD="app-password-test",
    )
    @patch("contacto.notificaciones._enviar_smtp", side_effect=RuntimeError("fallo SMTP controlado"))
    def test_fallo_smtp_se_registra_sin_interrumpir_la_solicitud(self, smtp):
        cotizacion = SolicitudCotizacion.objects.create(
            nombre="Cliente con fallo",
            telefono="0999999999",
            email="cliente@example.com",
            tipo_proyecto="aplicacion_web",
            descripcion="Necesito desarrollar una aplicación web para gestionar clientes.",
            preferencia_contacto="email",
        )
        estado = notificar_nueva_cotizacion(cotizacion)
        self.assertEqual(estado, SolicitudCotizacion.EstadoNotificacion.FALLIDA)
        smtp.assert_called_once()

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        EMAIL_HOST_USER="remitente@example.com",
        EMAIL_HOST_PASSWORD="credencial-de-prueba",
        DEFAULT_FROM_EMAIL="CODEHAVEN <remitente@example.com>",
        COTIZACIONES_EMAIL="ochoaesteban593@gmail.com",
    )
    def test_correo_profesional_se_dirige_al_destinatario_solicitado(self):
        cotizacion = SolicitudCotizacion.objects.create(
            nombre="Cliente de prueba",
            empresa="Negocio de prueba",
            telefono="0999999999",
            email="cliente@example.com",
            tipo_proyecto="aplicacion_web",
            descripcion="Necesito desarrollar un sistema web para administrar mi negocio.",
            preferencia_contacto="whatsapp",
        )
        asunto, html, texto = _contenido_notificacion(cotizacion)
        _enviar_smtp(cotizacion, asunto, html, texto)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["ochoaesteban593@gmail.com"])
        self.assertEqual(mail.outbox[0].subject, "Nueva solicitud de cotización - Cliente de prueba")
        self.assertIn("Necesito desarrollar un sistema web", mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].alternatives[0].mimetype, "text/html")

    def test_solicitud_es_visible_en_admin(self):
        user = get_user_model().objects.create_superuser(
            username="admin-test", email="admin@example.com", password="test-pass-12345"
        )
        SolicitudCotizacion.objects.create(
            nombre="Cliente de prueba",
            telefono="0999999999",
            email="cliente@example.com",
            tipo_proyecto="aplicacion_web",
            descripcion="Necesito desarrollar un sistema web para administrar mi negocio.",
            preferencia_contacto="whatsapp",
        )
        self.client.force_login(user)
        response = self.client.get("/admin/contacto/solicitudcotizacion/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cliente de prueba")
        self.assertContains(response, "Aplicación web")

    @override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"])
    def test_pagina_404_personalizada(self):
        response = self.client.get("/ruta-inexistente/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Página no encontrada", status_code=404)
