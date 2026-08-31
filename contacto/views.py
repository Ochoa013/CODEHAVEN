from urllib.parse import quote

from django.shortcuts import render


WHATSAPP_NUMBER = "593969048598"
WHATSAPP_MESSAGE = (
    "Hola, Esteban. Me interesa una solución de software para mi negocio. "
    "Quisiera contarte brevemente la necesidad que deseo resolver."
)
LEGAL_WHATSAPP_MESSAGE = (
    "Hola, Esteban. Necesito orientación sobre un asunto legal y quisiera "
    "solicitar una consulta."
)


def whatsapp_url(message=WHATSAPP_MESSAGE):
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(message)}"


def page_context():
    return {"whatsapp_url": whatsapp_url()}


def service_selector(request):
    return render(request, "portfolio/services.html")


def perfil_profesional(request):
    return render(request, "portfolio/perfil_profesional.html", page_context())


def desarrollo_web(request):
    return render(request, "portfolio/home.html", page_context())



def asesoria_legal(request):
    return render(
        request,
        "portfolio/legal.html",
        {"whatsapp_url": whatsapp_url(LEGAL_WHATSAPP_MESSAGE)},
    )


def custom_404(request, exception=None):
    return render(
        request,
        "404.html",
        {"whatsapp_url": whatsapp_url()},
        status=404,
    )
