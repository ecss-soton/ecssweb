"""
Django settings for ecssweb project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret_key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


SERVER_EMAIL = 'ecssweb@example.com'
EMAIL_SUBJECT_PREFIX = '[ECSSWEB] '


ADMINS = [('Example', 'example@example.com')]


ALLOWED_HOSTS = ['localhost']


# Sites
SITE_ID = 1


# Set to None to use session-based CSRF cookies
# https://docs.djangoproject.com/en/2.0/ref/settings/#csrf-cookie-age
CSRF_COOKIE_AGE = None

CSRF_COOKIE_SECURE = False


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'website.apps.WebsiteConfig',
    'ecsswebauth.apps.EcsswebauthConfig',
    'ecsswebadmin.apps.EcsswebadminConfig',
    'portal.apps.PortalConfig',
    'feedback.apps.FeedbackConfig',
    'auditlog.apps.AuditlogConfig',
    'fbevents.apps.FbeventsConfig',
    'jumpstart.apps.JumpstartConfig',
    'shop.apps.ShopConfig',
    'election.apps.ElectionConfig',
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

ROOT_URLCONF = 'ecssweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'ecssweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Auth

AUTHENTICATION_BACKENDS = [
    'ecsswebauth.backends.SamlBackend',
]

LOGIN_REDIRECT_URL = 'portal:overview'

LOGIN_URL = 'ecsswebauth:auth'

LOGOUT_REDIRECT_URL = 'ecsswebauth:auth'


# Messages

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


# Sessions

SESSION_COOKIE_SECURE = False

SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# Logging
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     'mail_admins': {
#         'level': 'ERROR',
#         'class': 'django.utils.log.AdminEmailHandler',
#     },
# },
# 'loggers': {
#     'django': {
#         'handlers': ['console', 'mail_admins'],
#             'level': 'WARN',
#             'propagate': True,
#         },
#     },
# }


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = ''

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# SAML

# SAML config file folders
SAML_FOLDER = os.path.join(BASE_DIR, 'ecsswebauth', 'saml_config')

SAML_GROUP_PREFIX = 'saml_'


# FB

FB_PAGE_ID = ''

FB_ACCESS_TOKEN = ''


# Face Detection

FACE_DETECT_ENABLED = False

FACE_DETECT_API = ''
