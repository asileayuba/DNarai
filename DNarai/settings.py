from pathlib import Path
from dotenv import load_dotenv
import os
import dj_database_url
from celery.schedules import crontab

# Load environment variables
load_dotenv()

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================
# Security
# ==========================
SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-secret-key")
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# ==========================
# Custom User Model
# ==========================
AUTH_USER_MODEL = "accounts.CustomUser"

AUTHENTICATION_BACKENDS = [
    "accounts.auth_backends.UsernameOrEmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# ==========================
# Installed Apps
# ==========================
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps
    "accounts",
    "core",

    # Celery
    "django_celery_results",
    "django_celery_beat",
]

# ==========================
# Middleware
# ==========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "DNarai.urls"

# ==========================
# Templates
# ==========================
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

WSGI_APPLICATION = "DNarai.wsgi.application"
ASGI_APPLICATION = "DNarai.asgi.application"  # For Channels/Daphne if used

# ==========================
# Database
# ==========================
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

# ==========================
# Password Validation
# ==========================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==========================
# Internationalization
# ==========================
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

# ==========================
# Static & Media
# ==========================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "core/static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==========================
# Email
# ==========================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() in ("true", "1", "yes")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "DNarai <no-reply@dnarai.com>")

DEFAULT_MENTOR_EMAIL = os.getenv("DEFAULT_MENTOR_EMAIL", "admin@example.com")
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

# ==========================
# Celery
# ==========================
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "django-db")
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BEAT_SCHEDULE = {
    "run-every-10-mins": {
        "task": "DNarai.tasks.send_email_task",
        "schedule": crontab(minute="*/10"),
    },
}

# ==========================
# Logging
# ==========================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "mentorship_app.log",
            "formatter": "verbose",
        },
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {"handlers": ["file", "console"], "level": "INFO", "propagate": True},
        "core": {"handlers": ["file", "console"], "level": "INFO", "propagate": False},
    },
}

# ==========================
# Auth Redirects
# ==========================
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "/"
