import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.environ.get("SECRET_KEY", "inseguro-en-local")
# Para desarrollo puedes dejar DEBUG=True en tu entorno local, en producción obligatoriamente DEBUG=False
DEBUG = os.environ.get("DEBUG", "True") == "True"

# ALLOWED_HOSTS: si pones "*" en la variable de entorno se mantendrá el wildcard,
# si no se toman los hosts de la variable ALLOWED_HOSTS separada por comas,
# o por defecto localhost y 127.0.0.1 para desarrollo.
_raw_allowed = os.environ.get("ALLOWED_HOSTS", None)
if _raw_allowed:
    if _raw_allowed.strip() == "*":
        ALLOWED_HOSTS = ["*"]
    else:
        ALLOWED_HOSTS = [h.strip() for h in _raw_allowed.split(",") if h.strip()]
else:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Aplicaciones
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tareas",
    "users",
    "alumnos",
    "scraper",
    "contacto",
    "informes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # sirve para servir estáticos en producción
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "crud.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "crud.wsgi.application"

# DATABASES
# - Por defecto usa sqlite para desarrollo
# - Si existe DATABASE_URL en el entorno, dj_database_url la usará (ideal para Render/Heroku)
DATABASE_URL = os.environ.get("DATABASE_URL", None)
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=not DEBUG)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

# STATIC FILES
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# AUTH / REDIRECT
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "login"

# EMAIL
# - Por defecto, en desarrollo usamos el backend de consola (no enviar correos reales).
# - En producción, pon EMAIL_HOST en las environment variables para activar SMTP.
if os.environ.get("EMAIL_HOST"):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.environ.get("EMAIL_HOST")
    EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
    EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
    # Si usas otros proveedores (SSL) ajusta EMAIL_USE_SSL/ports según corresponda.
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "no-reply@example.com")

# Mensajes
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

# Seguridad adicional para despliegues detrás de un proxy (ej. Render)
# Asegúrate de habilitar esto si tu plataforma setea X-Forwarded-Proto
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Opcional: ajustes de seguridad que conviene activar en producción
if not DEBUG:
    # Forzar HTTPS (configurable via env)
    SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "True") == "True"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # HSTS
    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", 60))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get("SECURE_HSTS_INCLUDE_SUBDOMAINS", "True") == "True"
    SECURE_HSTS_PRELOAD = os.environ.get("SECURE_HSTS_PRELOAD", "False") == "True"

# Logging básico (puedes ampliarlo según necesidades)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO")},
}