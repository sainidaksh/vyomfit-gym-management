# core/settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ==================================================
# BASIC
# ==================================================
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "render-secret-key")

DEBUG = False   # 🔴 RENDER = FALSE

# ==================================================
# ALLOWED HOSTS (RENDER FIX)
# ==================================================
ALLOWED_HOSTS = [
    "vyomfit.onrender.com",
    ".onrender.com",
    "localhost",
    "127.0.0.1",
]

# ==================================================
# CSRF (RENDER FIX)
# ==================================================
CSRF_TRUSTED_ORIGINS = [
    "https://vyomfit.onrender.com",
]

# ==================================================
# APPLICATIONS
# ==================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
