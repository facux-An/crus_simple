import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.environ.get("SECRET_KEY", "inseguro-en-local")
# Para desarrollo puedes dejar DEBUG=True en tu entorno local, en producción obligatoriamente DEBUG=False
DEBUG = os.environ.get("DEBUG", "True") == "True"

# ALLOWED_HOSTS
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

# ---------------------------------------------------------------------
# EMAIL (Mailgun via Anymail preferred) - fallback a SMTP si se configura
# ---------------------------------------------------------------------
# Prioridad:
# 1) Si MAILGUN_API_KEY y MAILGUN_DOMAIN están definidos -> usar Anymail + Mailgun (API)
# 2) elif EMAIL_HOST está definido -> usar SMTP (como antes)
# 3) else -> backend de consola (desarrollo)

MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
# DEFAULT_FROM_EMAIL puede venir del entorno; si no, se construye más abajo según el backend seleccionado.
DEFAULT_FROM_EMAIL_ENV = os.environ.get("DEFAULT_FROM_EMAIL")

# Si está configurado Mailgun (API) lo utilizamos
if MAILGUN_API_KEY and MAILGUN_DOMAIN:
    # Asegúrate de añadir 'anymail' a requirements.txt (pip install anymail)
    if "anymail" not in INSTALLED_APPS:
        INSTALLED_APPS.append("anymail")

    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
    ANYMAIL = {
        "MAILGUN_API_KEY": MAILGUN_API_KEY,
        # opcionalmente: "MAILGUN_API_URL": os.environ.get("MAILGUN_API_URL", "https://api.mailgun.net/v3"),
        # y también "MAILGUN_SENDER_DOMAIN" = MAILGUN_DOMAIN si lo necesitas explícitamente
        "MAILGUN_SENDER_DOMAIN": MAILGUN_DOMAIN,
    }
    DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL_ENV or f"postmaster@{MAILGUN_DOMAIN}"

# Si no hay Mailgun definido, permitimos SMTP si se definieron variables
elif os.environ.get("EMAIL_HOST"):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.environ.get("EMAIL_HOST")
    EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
    EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
    EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "False") == "True"
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
    DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL_ENV or EMAIL_HOST_USER or "no-reply@example.com"
    # Nota: si usas Gmail y Render no permite SMTP, es preferible pasar a Mailgun/SendGrid.
else:
    # Desarrollo / fallback: backend de consola
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL_ENV or "no-reply@example.com"

# Mensajes
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

# Seguridad adicional para despliegues detrás de un proxy (ej. Render)
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

# Logging básico
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO")},
}