from .base import *

DEFENDER_MOCK_REDIS = True

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
