# ------------------------------- Environ Setup ----------------------------- #
import os
import environ

ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('apps')
ROOT_NAME = "hackncast"

env = environ.Env()
environ.Env.read_env()

# ------------------------------- Basic Setup ------------------------------- #
SITE_ID = 1
DEBUG = env.bool('DJANGO_DEBUG', default=False)
WSGI_APPLICATION = '{}.wsgi.application'.format(ROOT_NAME)

# Internationalization
LANGUAGES = (
    ("pt-br", "Português do Brasil"),
    ("en", "Inglês"),
)
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = str(ROOT_DIR('staticfiles'))
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    str(ROOT_DIR.path('../frontend/static')),
)

# Media files
MEDIA_ROOT = str(ROOT_DIR('media'))
MEDIA_URL = '/media/'

# URLs
ROOT_URLCONF = '{}.urls'.format(ROOT_NAME)
APPEND_SLASH = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    },
}
# ----------------------------- Security Setup ------------------------------ #
SECRET_KEY = env('DJANGO_SECRET_KEY', default='')

ALLOWED_HOSTS = []

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.'
     'UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.'
     'MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.'
     'CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.'
     'NumericPasswordValidator'},
]

# ---------------------------------- Apps ----------------------------------- #
DJANGO_APPS = (
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
)

LOCAL_APPS = (
)

# -------------------- Middlewares & Templates Settings --------------------- #
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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

# ------------------------ Third Party App Settings ------------------------- #
# ALLAUTH SETTINGS
# Use email for login
ACCOUNT_AUTHENTICATION_METHOD = "email"
# Unverified email can't login
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
SOCIALACCOUNT_EMAIL_VERIFICATION = ACCOUNT_EMAIL_VERIFICATION
# User must inform email
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED
# User must inform username during singup
ACCOUNT_USERNAME_REQUIRED = False

# -------------------------- Custom Site Settings --------------------------- #
