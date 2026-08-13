from datetime import timedelta
from urllib.parse import quote

from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from .forms import SolicitudCotizacionForm
from .models import SolicitudCotizacion
from .notificaciones import notificar_nueva_cotizacion


WHATSAPP_NUMBER = "593969048598"
WHATSAPP_MESSAGE = (
    "Hola, Esteban. Estoy interesado/a en desarrollar un proyecto de software "
    "y quisiera recibir más información."
)


def whatsapp_url(message=WHATSAPP_MESSAGE):
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(message)}"


def page_context(request=None, form=None):
    confirmation = None
    if request and request.GET.get("solicitud") == "recibida":
        confirmation = request.session.pop("cotizacion_confirmada", None)
    return {
        "form": form or SolicitudCotizacionForm(),
        "whatsapp_url": whatsapp_url(),
        "cotizacion_confirmada": confirmation,
    }


def home(request):
    return render(request, "portfolio/home.html", page_context(request))


@require_POST
@csrf_protect
def solicitar_contacto(request):
    form = SolicitudCotizacionForm(request.POST)
    if form.is_valid():
        duplicate_since = timezone.now() - timedelta(minutes=2)
        duplicate_exists = SolicitudCotizacion.objects.filter(
            email=form.cleaned_data["email"],
            descripcion=form.cleaned_data["descripcion"],
            fecha_solicitud__gte=duplicate_since,
        ).exists()
        if duplicate_exists:
            form.add_error(
                None,
                "Esta solicitud ya fue recibida. Evita enviarla nuevamente; pronto será revisada.",
            )
        else:
            cotizacion = form.save()
            notificar_nueva_cotizacion(cotizacion)
            project_name = cotizacion.get_tipo_proyecto_display()
            fast_message = (
                "Hola Esteban, acabo de enviar una solicitud de cotización desde tu "
                f"página web. Mi nombre es {cotizacion.nombre} y estoy interesado/a en "
                f"{project_name}."
            )
            request.session["cotizacion_confirmada"] = {
                "nombre": cotizacion.nombre,
                "proyecto": project_name,
                "whatsapp_url": whatsapp_url(fast_message),
            }
            return redirect(f"{reverse('home')}?solicitud=recibida#contacto")

    return render(request, "portfolio/home.html", page_context(request, form), status=422)


def custom_404(request, exception=None):
    return render(
        request,
        "404.html",
        {"whatsapp_url": whatsapp_url()},
        status=404,
    )
