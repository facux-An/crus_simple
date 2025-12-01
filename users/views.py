from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django import forms
from django.conf import settings
from smtplib import SMTPException

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

            # Enviar correo de bienvenida (manejo de errores)
            subject = "Bienvenido al sistema de Alumnos"
            message = f"Hola {user.username}, tu registro fue exitoso. ¡Bienvenido!"
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)

            try:#
                import logging
                logger = logging.getLogger(__name__)

                logger.info("EMAIL_BACKEND=%s EMAIL_HOST=%s", getattr(settings, "EMAIL_BACKEND", None), getattr(settings, "EMAIL_HOST", None))
                #
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                mail_sent = True
            except (BadHeaderError, SMTPException, Exception) as e:
                # No queremos bloquear el registro por un fallo en el envío de correo.
                mail_sent = False
                # Guardar info en mensajes para que el usuario lo sepa
                messages.warning(
                    request,
                    "Se registró correctamente, pero no se pudo enviar el correo de bienvenida (error de envío)."
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
                else:
                    # Warning ya agregado arriba en excepción; aquí podemos agregar info adicional opcional.
                    pass

            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})