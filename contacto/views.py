from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import ContactoForm

def contacto(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            email = form.cleaned_data["email"]
            mensaje = form.cleaned_data["mensaje"]

            cuerpo = f"Mensaje de {nombre} <{email}>:\n\n{mensaje}"
            print(f"""
            📨 Enviando correo:
            De: {email}
            para: {settings.EMAIL_HOST_USER}
            Asunto: Nuevo mensaje de contacto
            mensaje:
            {mensaje}
            """)      
            send_mail(
                subject="Nuevo mensaje de contacto",
                message=cuerpo,
                from_email=email,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            print("✅ Correo enviado")

            # Mostrar mensaje en la web
            messages.success(
                request,
                f"📨 Correo enviado correctamente desde {email} con asunto 'Nuevo mensaje de contacto'."
            )
            return redirect("dashboard")  # redirige al dashboard para ver el cartel
    else:
        form = ContactoForm()
    return render(request, "contacto/contacto.html", {"form": form})
