# core/settings.py

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ==================================================
# BASIC SETTINGS
# ==================================================

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-secret-key-change-later"
)

DEBUG = os.environ.get("DJANGO_DEBUG", "True").lower() in ("1", "true", "yes")

# ==================================================
# ALLOWED HOSTS (NGROK FIX)
# ==================================================

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".ngrok-free.dev",
    ".ngrok-free.app",
]

# ==================================================
# CSRF (NGROK FIX)
# ==================================================

CSRF_TRUSTED_ORIGINS = [
    "https://*.ngrok-free.dev",
    "https://*.ngrok-free.app",
]

# ==================================================
# APPLICATIONS
# ==================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # your apps
    'gyms',
    'members',
    'plans',
    'subscriptions',
    'attendance',
    'notifications',
    'payments',
]

# ==================================================
# MIDDLEWARE
# ==================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# ==================================================
# TEMPLATES
# ==================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.notifications_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# ==================================================
# DATABASE (LOCAL)
# ==================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==================================================
# AUTH
# ==================================================

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# ==================================================
# STATIC FILES
# ==================================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==================================================
# SECURITY (SAFE FOR NGROK DEV)
# ==================================================

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

SECURE_SSL_REDIRECT = False

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

X_FRAME_OPTIONS = 'DENY'
