from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("alumnos.urls")),
    path("users/", include("users.urls")),
    path("scraper/", include("scraper.urls")),
    path("contacto/", include("contacto.urls")),
    path("informes/", include(("informes.urls", "informes"), namespace="informes")),


]
