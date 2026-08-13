from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("contacto/solicitar/", views.solicitar_contacto, name="solicitar_contacto"),
]
