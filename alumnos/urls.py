from django.urls import path
from .views import (
    dashboard,
    crear_alumno,
    editar_alumno,
    borrar_alumno,
    enviar_pdf_alumno,
)

urlpatterns = [
    # Página principal del dashboard de alumnos
    path("", dashboard, name="dashboard"),

    # CRUD de alumnos
    path("crear/", crear_alumno, name="crear_alumno"),
    path("<int:alumno_id>/editar/", editar_alumno, name="editar_alumno"),
    path("<int:alumno_id>/borrar/", borrar_alumno, name="borrar_alumno"),

    # Generación y envío de PDF por correo
    path("pdf/<int:alumno_id>/", enviar_pdf_alumno, name="enviar_pdf_alumno"),
]
