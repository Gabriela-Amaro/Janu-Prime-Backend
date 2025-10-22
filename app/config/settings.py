import os
import logging

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is required")

ENV = os.getenv("DJANGO_ENV", "development")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV == "development"

ALLOWED_HOSTS = [host for host in os.getenv("ALLOWED_HOSTS", "").split(",") if host]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-Party Apps
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "django_filters",
    # My Apps
    "core",
    "usuarios.apps.UsuariosConfig",
    "estabelecimentos",
    "produtos",
    "transacoes",
    "avaliacoes",
    "anuncios",
    "logs",
]

AUTH_USER_MODEL = "usuarios.Usuario"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": "db",  # nome do serviço no docker-compose.yml
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",  # <- pasta dentro do projeto
]
STATIC_ROOT = (
    BASE_DIR / "staticfiles"
)  # <- pasta onde o collectstatic vai jogar os arquivos

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- REST FRAMEWORK, JWT & CORS CONFIGURATIONS ---
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Frontend
    "http://127.0.0.1:3000",
    "http://localhost:8000",  # Django admin
    "http://127.0.0.1:8000",
]

# Configurações de segurança CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False  # Nunca True em produção

# Configurações do Django Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

SIMPLE_JWT = {
    # === PARA DESENVOLVIMENTO (facilitar testes) ===
    "ACCESS_TOKEN_LIFETIME": (
        timedelta(days=1) if ENV == "development" else timedelta(minutes=5)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# --- CONFIGURAÇÕES DE SEGURANÇA BÁSICAS ---
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# Configurações de logging para desenvolvimento
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "estabelecimento_context": {
            "()": "core.logging_filters.EstabelecimentoContextFilter",
        },
    },
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} | {module} | estabelecimento={estabelecimento_id} | {message}",
            "style": "{",
            "datefmt": "%d-%m-%Y %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["estabelecimento_context"],
        },
        # só será ativado em produção
        "loki": {
            "class": "logging.NullHandler",  # placeholder, será substituído em produção
            "formatter": "verbose",
            "filters": ["estabelecimento_context"],
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "app": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

# 🔹 Se estiver em produção, troca o handler "loki" para um real
if ENV == "production":
    try:
        # baixar o handler do loki
        from loki_django_logger.handler import AsyncGzipLokiHandler

        LOGGING["handlers"]["loki"] = {
            "class": "loki_django_logger.handler.AsyncGzipLokiHandler",
            "loki_url": os.getenv("LOKI_URL", "http://localhost:3100"),
            "labels": {
                "application": "meuapp",
                "environment": ENV,
            },
            "level": "INFO",
            "formatter": "verbose",
        }

        # adiciona loki a todos os loggers
        LOGGING["root"]["handlers"].append("loki")
        LOGGING["loggers"]["django"]["handlers"].append("loki")
        LOGGING["loggers"]["meuapp"]["handlers"].append("loki")

    except ImportError:
        # Se ainda não tem loki_django_logger instalado, ignora
        logging.warning("Loki handler não configurado (pacote não instalado).")
