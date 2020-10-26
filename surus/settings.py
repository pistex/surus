"""
Django settings for surus project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path
from apps.gcp.secret_manager import get_secret_version
from corsheaders.defaults import default_headers
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = get_secret_version(
    'projects/808537418853/secrets/DJANGO_SECRET_KEY/versions/1')
DEBUG = False
ALLOWED_HOSTS = [
    get_secret_version('projects/808537418853/secrets/ALLOWED_HOSTS/versions/1')
    ]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'surus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'surus.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret_version(
            'projects/808537418853/secrets/POSTGRES_DB/versions/1'),
        'USER': get_secret_version(
            'projects/808537418853/secrets/POSTGRES_USER/versions/1'),
        'PASSWORD': get_secret_version(
            'projects/808537418853/secrets/POSTGRES_PASSWORD/versions/1'),
        'HOST': get_secret_version(
            'projects/808537418853/secrets/POSTGRES_HOST/versions/1'),
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/sbpann/surus/media/'

# Custom user model
INSTALLED_APPS += ['apps.user.apps.UserConfig']
AUTH_USER_MODEL = 'user.User'
AUTHENTICATION_BACKENDS = ['apps.user.authentication.ModelBackend']

# django-allauth
INSTALLED_APPS += [
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google'
]
AUTHENTICATION_BACKENDS += [
    'allauth.account.auth_backends.AuthenticationBackend',
    'apps.api.jwt_auth.JWTCookieAuthentication'
]
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': get_secret_version(
                'projects/808537418853/secrets/GOOGLE_CLIENT_ID/versions/1'),
            'secret': get_secret_version(
                'projects/808537418853/secrets/GOOGLE_SECRET_KEY/versions/1')
        }
    },
    'facebook': {
        'APP': {
            'client_id': get_secret_version(
                'projects/808537418853/secrets/FACEBOOK_CLIENT_ID/versions/1'),
            'secret': get_secret_version(
                'projects/808537418853/secrets/FACEBOOK_SECRET_KEY/versions/1')
        }
    }
}
SITE_ID = 1
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'surus.d6101@gmail.com'
EMAIL_HOST_PASSWORD = get_secret_version(
    'projects/808537418853/secrets/EMAIL_HOST_PASSWORD/versions/1')
EMAIL_USE_TLS = True
ACCOUNT_ADAPTER = 'apps.api.adapters.MyAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'apps.api.adapters.MySocialAccountAdapter'
FRONTEND_URL = 'https://surus-frontend-enj3kcn2iq-as.a.run.app/'

# blog app
INSTALLED_APPS += [
    'simple_history',
    'apps.blog.apps.BlogConfig'
]
MIDDLEWARE += ['simple_history.middleware.HistoryRequestMiddleware']

# api
INSTALLED_APPS += [
    'rest_framework',
    'django_filters',
    'apps.api.apps.ApiConfig'
]

# CORS
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE += [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]
CORS_ALLOWED_ORIGINS = [
    'https://surus-frontend-enj3kcn2iq-as.a.run.app'
]
CORS_ALLOW_HEADERS = list(default_headers) + [
    'backend-authorization',
]
# dj-rest-auth
INSTALLED_APPS += [
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration'
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.api.jwt_auth.JWTCookieAuthentication'
        ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
        ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'
        ]
}
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'surus-auth'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=4),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
}

# Google Cloud
INSTALLED_APPS += [
    'apps.gcp'
]
# Google Cloud Storage
# STATICFILES_STORAGE = 'apps.gcp.storage.StaticFile'
# no more static file needed.
DEFAULT_FILE_STORAGE = 'apps.gcp.storage.MediaFile'
# GS_STATIC_FILE_LOCATION = "static/"
# no more static file needed.
GS_MEDIA_FILE_LOCATION = "file/"
GS_BUCKET_NAME = 'surus'
GS_DEFAULT_ACL = 'publicRead'
GS_CUSTOM_ENDPOINT = 'https://surus.storage.googleapis.com'

# reCAPTCHA secret key
RECAPTCHA_SERVER_SECRET_KEY = get_secret_version(
    'projects/808537418853/secrets/RECAPTCHA_SERVER_SECRET_KEY/versions/1')
