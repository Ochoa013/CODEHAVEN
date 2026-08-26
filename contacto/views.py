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
LEGAL_WHATSAPP_MESSAGE = (
    "Hola, Esteban. Necesito orientación sobre un asunto legal y quisiera "
    "solicitar una consulta."
)


def whatsapp_url(message=WHATSAPP_MESSAGE):
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(message)}"


def page_context(request=None, form=None):
    notification_result = None
    if request and request.GET.get("solicitud") == "resultado":
        notification_result = request.session.pop("cotizacion_resultado", None)
    return {
        "form": form or SolicitudCotizacionForm(),
        "whatsapp_url": whatsapp_url(),
        "cotizacion_resultado": notification_result,
    }


def service_selector(request):
    return render(request, "portfolio/services.html")


def desarrollo_web(request):
    return render(request, "portfolio/home.html", page_context(request))


def asesoria_legal(request):
    return render(
        request,
        "portfolio/legal.html",
        {"whatsapp_url": whatsapp_url(LEGAL_WHATSAPP_MESSAGE)},
    )


@require_POST
@csrf_protect
def solicitar_contacto(request):
    form = SolicitudCotizacionForm(request.POST)
    if form.is_valid():
        duplicate_since = timezone.now() - timedelta(minutes=2)
        cotizacion = SolicitudCotizacion.objects.filter(
            email=form.cleaned_data["email"],
            descripcion=form.cleaned_data["descripcion"],
            fecha_solicitud__gte=duplicate_since,
        ).first()

        if cotizacion is None:
            cotizacion = form.save()

        notification_state = notificar_nueva_cotizacion(cotizacion)
        request.session["cotizacion_resultado"] = (
            "success"
            if notification_state
            == SolicitudCotizacion.EstadoNotificacion.ENVIADA_RESEND
            else "error"
        )
        return redirect(f"{reverse('desarrollo_web')}?solicitud=resultado#contacto")

    return render(request, "portfolio/home.html", page_context(request, form), status=422)


def custom_404(request, exception=None):
    return render(
        request,
        "404.html",
        {"whatsapp_url": whatsapp_url()},
        status=404,
    )
