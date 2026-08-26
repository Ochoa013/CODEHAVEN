from django.urls import path

from . import views


urlpatterns = [
    path("", views.service_selector, name="home"),
    path("desarrollo-web/", views.desarrollo_web, name="desarrollo_web"),
    path("asesoria-legal/", views.asesoria_legal, name="asesoria_legal"),
]
