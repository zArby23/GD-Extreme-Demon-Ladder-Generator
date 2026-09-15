import os
import secrets
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"
configured_secret_key = os.getenv("DJANGO_SECRET_KEY")
if not DEBUG and not configured_secret_key:
    raise RuntimeError("DJANGO_SECRET_KEY must be set in production")
SECRET_KEY = configured_secret_key or secrets.token_urlsafe(50)
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost,testserver"
    ).split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "rest_framework",
    "ladder",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AREDL_BASE_URL = os.getenv("AREDL_BASE_URL", "https://api.aredl.net/v2/api")
AREDL_REQUEST_TIMEOUT = int(os.getenv("AREDL_REQUEST_TIMEOUT", "10"))
AREDL_CACHE_TTL = int(os.getenv("AREDL_CACHE_TTL", "300"))
