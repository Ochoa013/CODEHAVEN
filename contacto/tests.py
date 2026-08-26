import time
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import signing
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import SolicitudCotizacion
from .notificaciones import (
    _contenido_notificacion,
    _enviar_resend,
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

    def test_portada_presenta_las_dos_areas_profesionales(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "¿Problemas legales?")
        self.assertContains(response, "¿Quieres optimizar tu negocio?")
        self.assertContains(response, reverse("asesoria_legal"))
        self.assertContains(response, reverse("desarrollo_web"))

    def test_desarrollo_web_carga_con_formulario_y_contenido_principal(self):
        response = self.client.get(reverse("desarrollo_web"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Convierte tu idea en")
        self.assertContains(response, "Solicitar cotización")
        self.assertContains(response, "CODEHAVEN")
        self.assertContains(response, "codehaven-wordmark")
        self.assertNotContains(response, "codehaven-logo.png")
        self.assertContains(response, "Carrusel de especialidades")
        self.assertNotContains(response, 'id="sobre-mi"')
        self.assertContains(response, "csrfmiddlewaretoken")
        self.assertContains(response, "jquery-validation@1.22.1")
        self.assertContains(response, 'id="quote-form" novalidate')
        self.assertContains(response, "Ej. nombre@empresa.com")
        self.assertContains(response, "Selecciona el servicio que necesitas")

    def test_asesoria_legal_carga_con_servicios_y_contacto(self):
        response = self.client.get(reverse("asesoria_legal"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Respaldo legal para tomar decisiones")
        self.assertContains(response, "Consulta y orientación")
        self.assertContains(response, "wa.me/593969048598")

    @patch(
        "contacto.views.notificar_nueva_cotizacion",
        return_value=SolicitudCotizacion.EstadoNotificacion.ENVIADA_RESEND,
    )
    def test_solicitud_valida_se_guarda_y_muestra_confirmacion(self, notify):
        response = self.client.post(reverse("solicitar_contacto"), self.valid_payload(), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SolicitudCotizacion.objects.count(), 1)
        notify.assert_called_once()
        self.assertContains(response, "¡Información enviada correctamente!")
        self.assertContains(response, 'data-status="success"')
        self.assertContains(response, "sweetalert2@11.26.25")

    @patch(
        "contacto.views.notificar_nueva_cotizacion",
        return_value=SolicitudCotizacion.EstadoNotificacion.FALLIDA,
    )
    def test_fallo_de_envio_guarda_solicitud_y_muestra_error_seguro(self, notify):
        response = self.client.post(reverse("solicitar_contacto"), self.valid_payload(), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SolicitudCotizacion.objects.count(), 1)
        notify.assert_called_once()
        self.assertContains(response, "No se pudo enviar la solicitud")
        self.assertContains(response, 'data-status="error"')
        self.assertNotContains(response, "Traceback")

    @override_settings(
        RESEND_API_KEY="re_test",
        RESEND_FROM_EMAIL="notificaciones@example.com",
        CONTACT_EMAIL="destino@example.com",
    )
    @patch("contacto.notificaciones.resend.Emails.send", return_value={"id": "email-id"})
    def test_post_redirect_get_limpia_formulario_y_evitar_registro_duplicado(self, resend_send):
        first = self.client.post(reverse("solicitar_contacto"), self.valid_payload())
        second = self.client.post(reverse("solicitar_contacto"), self.valid_payload())
        self.assertEqual(first.status_code, 302)
        self.assertEqual(second.status_code, 302)
        self.assertEqual(SolicitudCotizacion.objects.count(), 1)
        resend_send.assert_called_once()

        response = self.client.get(second.url)
        self.assertFalse(response.context["form"].is_bound)

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
        RESEND_API_KEY="re_test",
        RESEND_FROM_EMAIL="notificaciones@example.com",
        CONTACT_EMAIL="destino@example.com",
    )
    @patch("contacto.notificaciones._enviar_resend", return_value="resend-id")
    def test_resend_es_el_unico_proveedor_y_registra_el_envio(self, send_resend):
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
        self.assertEqual(estado, SolicitudCotizacion.EstadoNotificacion.ENVIADA_RESEND)
        self.assertEqual(cotizacion.notificacion_referencia, "resend-id")
        send_resend.assert_called_once()

    @override_settings(RESEND_API_KEY="", RESEND_FROM_EMAIL="", CONTACT_EMAIL="")
    @patch("contacto.notificaciones._enviar_resend")
    def test_resend_sin_configuracion_no_intenta_enviar(self, send_resend):
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
        send_resend.assert_not_called()

    @override_settings(
        RESEND_API_KEY="re_test",
        RESEND_FROM_EMAIL="notificaciones@example.com",
        CONTACT_EMAIL="destino@example.com",
    )
    @patch("contacto.notificaciones._enviar_resend", side_effect=RuntimeError("fallo controlado"))
    def test_fallo_resend_se_registra_sin_exponer_detalle(self, send_resend):
        cotizacion = SolicitudCotizacion.objects.create(
            nombre="Cliente con fallo",
            telefono="0999999999",
            email="cliente@example.com",
            tipo_proyecto="aplicacion_web",
            descripcion="Necesito desarrollar una aplicación web para gestionar clientes.",
            preferencia_contacto="email",
        )
        with self.assertLogs("contacto.notificaciones", level="ERROR"):
            estado = notificar_nueva_cotizacion(cotizacion)
        cotizacion.refresh_from_db()
        self.assertEqual(estado, SolicitudCotizacion.EstadoNotificacion.FALLIDA)
        self.assertEqual(cotizacion.notificacion_detalle, "Resend no confirmó el envío.")
        self.assertNotIn("fallo controlado", cotizacion.notificacion_detalle)
        send_resend.assert_called_once()

    @override_settings(
        RESEND_API_KEY="re_test",
        RESEND_FROM_EMAIL="notificaciones@example.com",
        CONTACT_EMAIL="destino@example.com",
    )
    @patch("contacto.notificaciones.resend.Emails.send", return_value={"id": "email-id"})
    def test_correo_usa_solo_contact_email_y_cliente_como_reply_to(self, resend_send):
        cotizacion = SolicitudCotizacion.objects.create(
            nombre="Cliente de prueba",
            empresa="Negocio de prueba",
            telefono="0999999999",
            email="cliente@example.com",
            tipo_proyecto="aplicacion_web",
            descripcion="Necesito un sistema web <strong>privado</strong> para mi negocio.",
            preferencia_contacto="whatsapp",
        )
        asunto, html, texto = _contenido_notificacion(cotizacion)
        reference = _enviar_resend(cotizacion, asunto, html, texto)

        params, options = resend_send.call_args.args
        self.assertEqual(reference, "email-id")
        self.assertEqual(params["from"], "CODEHAVEN <notificaciones@example.com>")
        self.assertEqual(params["to"], ["destino@example.com"])
        self.assertEqual(params["reply_to"], "cliente@example.com")
        self.assertNotIn("cc", params)
        self.assertNotIn("bcc", params)
        self.assertEqual(
            params["subject"],
            "Nueva solicitud de desarrollo de software - Cliente de prueba",
        )
        self.assertIn("&lt;strong&gt;privado&lt;/strong&gt;", params["html"])
        self.assertNotIn("<strong>privado</strong>", params["html"])
        self.assertEqual(options["idempotency_key"], f"cotizacion-{cotizacion.pk}")

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
