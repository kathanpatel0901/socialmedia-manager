"""
Django settings for social_manager project.

Generated by 'django-admin startproject' using Django 4.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-49@##0%hf)79-s9k@8qybje)(87!_w7c&l8zdj+bll_$$%y^l)"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = [
    "127.0.0.1",
    "192.168.1.27",
    "socialmediamanager.in.net",
    "106.215.20.147",
    "127.0.0.0",
    "34.196.212.31",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # css
    "bootstrap5",
    "django_bootstrap5",
    "django_celery_beat",
    # forms_app
    "crispy_forms",
    "crispy_bootstrap5",
    # created_app
    "signin",
    # allauth_app
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # social_media
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.twitter_oauth2",
    "allauth.socialaccount.providers.linkedin_oauth2",
    "allauth.socialaccount.providers.github",
    # "social_django",
    # "allauth.socailaccount.providers.pinterest",
]

SITE_ID = 2

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # allauth
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "social_manager.urls"
import os

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # allauth
                "django.template.context_processors.request",
            ],
        },
    },
]


WSGI_APPLICATION = "social_manager.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME':'socialmedia-manager',
#         'USER':'admin09',
#         'PASSWORD':'KatPtl910411',
#         'HOST':'socialmedia-manager.cvcyeo2eczmn.ap-south-1.rds.amazonaws.com',
#         'PORT':5432,
#         'OPTIONS': {
#             'options': '-c search_path=public',
#         },

#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL = 'static/'

# STATICFILES_DIRS = [
#   BASE_DIR /'static'
# ]

STATIC_URL = "static/"

STATIC_ROOT = "staticfiles"  # os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static/"), "static"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

# allauth
AUTHENTICATION_BACKEND = [
    "django.conntrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# client_id = 1026452319339-k4h5fshgoaamj3o4uua9t02ckvl4asfp.apps.googleusercontent.com

# client_secrate = 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

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
            "https://www.googleapis.com/auth/user.birthday.read",
            "https://www.googleapis.com/auth/user.gender.read",
            "https://www.googleapis.com/auth/user.phonenumbers.read",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
            "FETCH_USERINFO": True,
        },
        "OAUTH_PKCE_ENABLED": True,
    },
    "facebook": {
        "METHOD": "oauth2",  # Set to 'js_sdk' to use the Facebook connect SDK
        "SDK_URL": "//connect.facebook.net/{locale}/sdk.js",
        "SCOPE": ["email", "public_profile"],
        "AUTH_PARAMS": {"auth_type": "reauthenticate"},
        "INIT_PARAMS": {"cookie": True},
        "FIELDS": [
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "name",
            "name_format",
            "picture",
            "short_name",
        ],
        "EXCHANGE_TOKEN": True,
        "LOCALE_FUNC": "path.to.callable",
        "VERIFIED_EMAIL": False,
        "VERSION": "v13.0",
        "GRAPH_API_URL": "https://graph.facebook.com/v13.0",
    },
    "linkedin": {
        "SCOPE": ["r_basicprofile", "r_emailaddress"],
        "PROFILE_FIELDS": [
            "id",
            "first-name",
            "last-name",
            "email-address",
            "picture-url",
            "public-profile-url",
        ],
    },
    "github": {
        "SCOPE": [
            "user",
            "repo",
            "read:org",
        ],
    },
    "pinterest": {
        "SCOPE": ["user_accounts:read"],
        "API_VERSION": "v5",
    },
}


# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_AUTHENTICATION_METHOD = 'email'
LOGIN_REDIRECT_URL = "/social_account"
LOGOUT_REDIRECT_URL = "/index"

# SOCIALACCOUNT_ADAPTER = 'signin.adapters.google_adapter.GoogleSocialAccountAdapter'

# SOCIALACCOUNT_ADAPTER = 'signin.adapters.twitter_adapter.TwitterSocialAccountAdapter'

TWITTER_API_KEY = "K6j9cjrkcddpNgLZcurk627tE"
TWITTER_API_SECRET_KEY = "7avCQF3YcfyazKiLMXA7LRKo4nV6P67Syxj0J5BYflzeNcY6iv"
TWITTER_ACCESS_TOKEN = "1758379615968514048-g8GOVnszAiBdUZo3XqZbRrVM66Gk5z"
TWITTER_ACCESS_TOKEN_SECRET = "SMfpOOTSu7vzTgzV0008bfdndv7TQJSnXzWgwznGqRJuN"

# celery Settings


# SECURE_SSL_REDIRECT = True
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_HSTS_SECONDS = 31536000  # One year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# CSRF_USE_SESSIONS = True
# .

#  gunicorn --bind 0.0.0.0:8000 social_manager.wsgi:application

# [program:gunicorn]
# directory=/home/ubuntu/clone
# command=/home/ubuntu/env/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/Social_Media_Manager/app.sock social_manager.wsgi:application
# autostart=true
# autorestart=true
# stderr_logfile=/var/log/gunicorn/gunicorn.err.log
# stdout_logfile=/var/log/gunicorn/gunicorn.out.log
# [group:guni]
# programs:gunicorn

# settings.py
from datetime import timedelta


CELERY_BROKER_URL = "redis://localhost:6379/0"

CELERY_BEAT_SCHEDULE = {
    "my-periodic-task": {
        "task": "signin.tasks.my_periodic_task",
        "schedule": timedelta(minutes=1),  # Adjust interval as needed
    },
}
