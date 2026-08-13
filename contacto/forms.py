import re
import time

from django import forms
from django.core import signing
from django.core.exceptions import ValidationError

from .models import SolicitudCotizacion


class SolicitudCotizacionForm(forms.ModelForm):
    website = forms.CharField(
        required=False,
        label="Sitio web",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "tabindex": "-1",
                "aria-hidden": "true",
            }
        ),
    )
    started_at = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = SolicitudCotizacion
        fields = (
            "nombre",
            "empresa",
            "telefono",
            "email",
            "tipo_proyecto",
            "presupuesto",
            "descripcion",
            "preferencia_contacto",
        )
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "placeholder": "Ej. Juan Pérez",
                    "autocomplete": "name",
                    "minlength": "2",
                    "maxlength": "80",
                }
            ),
            "empresa": forms.TextInput(
                attrs={
                    "placeholder": "Ej. Mi Empresa S.A.",
                    "autocomplete": "organization",
                    "maxlength": "120",
                }
            ),
            "telefono": forms.TextInput(
                attrs={
                    "placeholder": "Ej. 0991234567",
                    "autocomplete": "tel",
                    "inputmode": "numeric",
                    "pattern": "[0-9]{7,15}",
                    "minlength": "7",
                    "maxlength": "15",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "ejemplo@correo.com",
                    "autocomplete": "email",
                    "maxlength": "254",
                }
            ),
            "tipo_proyecto": forms.Select(attrs={"autocomplete": "off"}),
            "presupuesto": forms.TextInput(
                attrs={
                    "placeholder": "Rango o valor estimado (opcional)",
                    "maxlength": "80",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "placeholder": "Describe brevemente qué necesitas, qué problema deseas solucionar y las principales funciones que debería tener tu sistema.",
                    "rows": "7",
                    "minlength": "30",
                    "maxlength": "4000",
                }
            ),
            "preferencia_contacto": forms.RadioSelect,
        }
        error_messages = {
            "nombre": {"required": "Indica tu nombre para poder contactarte."},
            "telefono": {"required": "Indica un número de teléfono."},
            "email": {
                "required": "Indica un correo electrónico.",
                "invalid": "Escribe un correo electrónico válido.",
            },
            "tipo_proyecto": {"required": "Selecciona el tipo de proyecto."},
            "descripcion": {"required": "Cuéntame brevemente sobre el proyecto que necesitas."},
            "preferencia_contacto": {"required": "Selecciona cómo prefieres que te contacte."},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tipo_proyecto"].choices = [
            ("", "Selecciona una opción"),
            *SolicitudCotizacion.TipoProyecto.choices,
        ]
        self.fields["started_at"].initial = signing.dumps(time.time(), salt="contact-form")
        for name, field in self.fields.items():
            if name not in {"website", "started_at", "preferencia_contacto"}:
                field.widget.attrs["class"] = "form-control"

    def clean_nombre(self):
        nombre = " ".join(self.cleaned_data["nombre"].split())
        allowed_punctuation = {"'", "-", "."}
        if len(nombre) < 2 or any(
            not (character.isalpha() or character.isspace() or character in allowed_punctuation)
            for character in nombre
        ):
            raise ValidationError(
                "El nombre solo puede contener letras, espacios, apóstrofes, puntos y guiones."
            )
        return nombre

    def clean_telefono(self):
        telefono = self.cleaned_data["telefono"].strip()
        if not re.fullmatch(r"\d{7,15}", telefono):
            raise ValidationError("Ingresa entre 7 y 15 números, sin espacios ni símbolos.")
        return telefono

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()

    def clean_descripcion(self):
        descripcion = self.cleaned_data["descripcion"].strip()
        if len(descripcion) < 30:
            raise ValidationError(
                "Describe tu proyecto con un poco más de detalle (mínimo 30 caracteres)."
            )
        return descripcion

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("website"):
            raise ValidationError("No fue posible procesar la solicitud. Inténtalo nuevamente.")

        token = cleaned_data.get("started_at")
        try:
            started_at = float(
                signing.loads(token, salt="contact-form", max_age=172800)
            )
        except (signing.BadSignature, TypeError, ValueError):
            raise ValidationError(
                "La sesión del formulario expiró. Recarga la página e inténtalo nuevamente."
            )

        if time.time() - started_at < 2:
            raise ValidationError(
                "Espera un momento antes de enviar la solicitud e inténtalo nuevamente."
            )
        return cleaned_data
