from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django import forms
from django.conf import settings
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("El nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ese correo electrónico ya está registrado.")
        return email


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Crear usuario con contraseña encriptada
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Enviar correo de bienvenida
            subject = "Bienvenido al sistema de Alumnos"
            message = f"Hola {user.username}, tu registro fue exitoso. ¡Bienvenido!"
            from_email = settings.DEFAULT_FROM_EMAIL
            mail_sent = False

            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                mail_sent = True
            except BadHeaderError:
                messages.error(request, "Encabezado inválido en el correo.")
            except Exception as e:
                # Capturamos cualquier error de envío
                messages.warning(
                    request,
                    "Se registró correctamente, pero no se pudo enviar el correo de bienvenida."
                )

            # Autenticar y loguear al usuario
            user = authenticate(username=user.username, password=form.cleaned_data["password"])
            if user:
                login(request, user)
                if mail_sent:
                    messages.success(
                        request,
                        f"📨 Bienvenido {user.username}, se envió un correo de bienvenida a {user.email} ✅"
                    )

            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})
@staff_member_required  # solo accesible para usuarios staff/superusuario
def test_email(request):
    subject = "Prueba de Mailgun"
    message = "Este es un correo de prueba enviado desde Django usando Mailgun."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient = "tucorreo@ejemplo.com"  # cámbialo por tu email real

    try:
        send_mail(
            subject,
            message,
            from_email,
            [recipient],
            fail_silently=False,
        )
        return HttpResponse(f"✅ Correo de prueba enviado a {recipient}")
    except Exception as e:
        return HttpResponse(f"❌ Error al enviar correo: {e}")