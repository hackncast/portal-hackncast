from .base import *

DEBUG = True
MESSAGE_LEVEL = 0
MIDDLEWARE += ['silk.middleware.SilkyMiddleware']

TEMPLATE_DEBUG = False

THIRD_PARTY_APPS += (
    'django_extensions',
    'silk',
)

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
