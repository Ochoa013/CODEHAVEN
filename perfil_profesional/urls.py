from django.contrib import admin
from django.urls import include, path, re_path

from contacto import views


admin.site.site_header = "Administración | CODEHAVEN"
admin.site.site_title = "CODEHAVEN | Solicitudes"
admin.site.index_title = "Panel de solicitudes"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("contacto.urls")),
    re_path(r"^.*$", views.custom_404),
]

handler404 = views.custom_404
