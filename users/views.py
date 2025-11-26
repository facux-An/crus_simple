from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib import messages
from django import forms

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Crear usuario con contraseña encriptada
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Enviar correo de bienvenida
            send_mail(
                subject="Bienvenido al sistema de Alumnos",
                message=f"Hola {user.username}, tu registro fue exitoso. ¡Bienvenido!",
                from_email=None,  # usa DEFAULT_FROM_EMAIL de settings.py
                recipient_list=[user.email],
                fail_silently=False,
            )

            # Autenticar y loguear al usuario
            user = authenticate(username=user.username, password=form.cleaned_data["password"])
            if user:
                login(request, user)
                # Mensaje de bienvenida en pantalla
                messages.success(
                    request,
                    f"📨 Bienvenido {user.username}, se envió un correo de bienvenida a {user.email} ✅"
                )

            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})
