from .base import *

SILK = env('SILK', default=False)

DEBUG = True
MESSAGE_LEVEL = 0

if SILK:
    MIDDLEWARE.append('silk.middleware.SilkyMiddleware')
    THIRD_PARTY_APPS.append('silk')

TEMPLATE_DEBUG = False

THIRD_PARTY_APPS.append('django_extensions')

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
