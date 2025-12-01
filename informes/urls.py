from django.urls import path
from .views import reporte_pdf

app_name = "informes"

urlpatterns = [
    path("reporte/<int:id>/pdf/", reporte_pdf, name="reporte_pdf"),
]
