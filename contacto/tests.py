from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import SolicitudCotizacion


class SitioTests(TestCase):
    def test_portada_presenta_las_dos_areas_profesionales(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "¿Problemas legales?")
        self.assertContains(response, "¿Quieres optimizar tu negocio?")
        self.assertContains(response, reverse("asesoria_legal"))
        self.assertContains(response, reverse("desarrollo_web"))

    def test_desarrollo_web_ofrece_contacto_exclusivo_por_whatsapp(self):
        response = self.client.get(reverse("desarrollo_web"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Explícame el reto")
        self.assertContains(response, "Qué conviene contar")
        self.assertContains(response, "Hablemos por WhatsApp")
        self.assertContains(response, "wa.me/593969048598")
        self.assertNotContains(response, 'id="quote-form"')
        self.assertNotContains(response, "csrfmiddlewaretoken")
        self.assertNotContains(response, "Solicitud de proyecto")
        self.assertNotContains(response, "Correo electrónico")
        self.assertNotContains(response, 'href="tel:')
        self.assertNotContains(response, 'href="mailto:')

    def test_asesoria_legal_ofrece_contacto_exclusivo_por_whatsapp(self):
        response = self.client.get(reverse("asesoria_legal"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Respaldo legal para tomar decisiones")
        self.assertContains(response, "Consultar por WhatsApp")
        self.assertContains(response, "Cuéntanos tu situación por WhatsApp")
        self.assertContains(response, "wa.me/593969048598")
        self.assertNotContains(response, "<form")
        self.assertNotContains(response, 'href="tel:')
        self.assertNotContains(response, 'href="mailto:')

    def test_ruta_anterior_del_formulario_ya_no_existe(self):
        response = self.client.get("/contacto/solicitar/")
        self.assertEqual(response.status_code, 404)

    def test_solicitud_historica_es_visible_en_admin(self):
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
