from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO

from .models import Alumno
from .forms import AlumnoForm


@login_required
def dashboard(request):
    alumnos = Alumno.objects.filter(usuario=request.user).order_by("-creado")
    return render(request, "alumnos/dashboard.html", {"alumnos": alumnos})


@login_required
def crear_alumno(request):
    if request.method == "POST":
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.usuario = request.user
            alumno.save()
            messages.success(request, f"Alumno {alumno.nombre} creado correctamente ✅")
            return redirect("dashboard")
    else:
        form = AlumnoForm()
    return render(request, "alumnos/crear.html", {"form": form})


@login_required
def editar_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id, usuario=request.user)
    if request.method == "POST":
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            messages.success(request, f"Alumno {alumno.nombre} actualizado correctamente ✏️")
            return redirect("dashboard")
    else:
        form = AlumnoForm(instance=alumno)
    return render(request, "alumnos/editar.html", {"form": form, "alumno": alumno})


@login_required
def borrar_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id, usuario=request.user)
    if request.method == "POST":
        alumno.delete()
        messages.success(request, f"Alumno eliminado correctamente 🗑️")
        return redirect("dashboard")
    return redirect("dashboard")


@login_required
def enviar_pdf_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id, usuario=request.user)

    # Generar PDF en memoria (para enviar por email)
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)
    p.drawString(100, 800, "Datos del Alumno")
    p.drawString(100, 770, f"Nombre: {alumno.nombre}")
    p.drawString(100, 750, f"Email: {alumno.email}")
    p.drawString(100, 730, f"Carrera: {alumno.carrera}")
    p.drawString(100, 710, f"Creado: {alumno.creado.strftime('%d/%m/%Y %H:%M')}")
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    # Enviar correo con PDF adjunto
    email = EmailMessage(
        subject="Ficha del Alumno",
        body=f"Adjunto los datos del alumno {alumno.nombre}.",
        from_email=None,  # usa DEFAULT_FROM_EMAIL
        to=[request.user.email],  # o al docente
    )
    email.attach("alumno.pdf", pdf, "application/pdf")
    email.send()

    messages.success(request, f"Se envió el PDF de {alumno.nombre} por correo ✅")
    return redirect("dashboard")


@login_required
def descargar_pdf_alumno(request, alumno_id):
    """
    Genera y devuelve el PDF del alumno como descarga (attachment).
    """
    alumno = get_object_or_404(Alumno, id=alumno_id, usuario=request.user)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)
    p.drawString(100, 800, "Datos del Alumno")
    p.drawString(100, 770, f"Nombre: {alumno.nombre}")
    p.drawString(100, 750, f"Email: {alumno.email}")
    p.drawString(100, 730, f"Carrera: {alumno.carrera}")
    p.drawString(100, 710, f"Creado: {alumno.creado.strftime('%d/%m/%Y %H:%M')}")
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    from django.http import HttpResponse
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="alumno_{alumno.id}.pdf"'
    return response