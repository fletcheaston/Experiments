import sys
from pathlib import Path

from .env_settings import SETTINGS

################################################################################
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SETTINGS.secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = SETTINGS.debug

################################################################################
# Boring stuff
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

COLLECTING_STATIC = sys.argv[1:2] == ["collectstatic"]

# Arbitrarily high
DATA_UPLOAD_MAX_MEMORY_SIZE = 30000000
DATA_UPLOAD_MAX_NUMBER_FIELDS = None

################################################################################
# Sessions/CSRF
SESSION_COOKIE_SECURE = not SETTINGS.debug
CSRF_COOKIE_SECURE = not SETTINGS.debug

CSRF_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SAMESITE = "None"

# How many seconds the cookie will last
# 1209600 = 2 weeks
SESSION_COOKIE_AGE = 1209600

# True prevents client side JS from accessing the cookie
SESSION_COOKIE_HTTPONLY = True

CSRF_USE_SESSIONS = False

CSRF_TRUSTED_ORIGINS = [
    ############################################################################
    # Local dev
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8001",
    ############################################################################
    # Real domains
    "https://fletcheaston.com",
]

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True

CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken"]

CORS_ALLOWED_ORIGINS = [
    ############################################################################
    # Local dev
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8001",
    ############################################################################
    # Real domains
    "https://fletcheaston.com",
]

ALLOWED_HOSTS: list[str] = [
    ############################################################################
    # Local dev
    "localhost",
    ############################################################################
    # Real domains
    "fletcheaston.com",
]

################################################################################
# Application definition
AUTH_USER_MODEL = "app_users.User"

LOGIN_URL = "/login/"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

INSTALLED_APPS = [
    ############################################################################
    # Has to be first for the User auth model
    "app_users",
    ############################################################################
    # Django's builtin apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    ############################################################################
    # Third-party apps
    "simple_history",
    "django_extensions",
    ############################################################################
    # Custom apps
    "app_blog",
    "app_advent_of_code",
    "app_my_freight_cube",
]

MIDDLEWARE = [
    ############################################################################
    # Django's builtin middleware
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    ############################################################################
    # Third-party middleware
    "simple_history.middleware.HistoryRequestMiddleware",
    ############################################################################
    # Custom middleware
]


ROOT_URLCONF = "server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "server.wsgi.application"

################################################################################
# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": SETTINGS.sql_database_name,
        "USER": SETTINGS.sql_database_user,
        "PASSWORD": SETTINGS.sql_database_password,
        "HOST": SETTINGS.sql_database_host,
        "PORT": 5432,
    },
}

################################################################################
# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "django_cache",
    },
}

################################################################################
# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

################################################################################
# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

STATICFILES_DIRS = [BASE_DIR / "app_blog/static"]

################################################################################
# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True
