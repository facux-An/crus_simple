from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("crear/", views.crear_alumno, name="crear_alumno"),
    path("editar/<int:alumno_id>/", views.editar_alumno, name="editar_alumno"),
    path("borrar/<int:alumno_id>/", views.borrar_alumno, name="borrar_alumno"),
    path("enviar-pdf/<int:alumno_id>/", views.enviar_pdf_alumno, name="enviar_pdf_alumno"),
    path("descargar-pdf/<int:alumno_id>/", views.descargar_pdf_alumno, name="descargar_pdf_alumno"),
]