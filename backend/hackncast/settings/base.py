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
    str(ROOT_DIR.path('../frontend/dist/static/')),
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
     'NumericPasswordValidator'},
    {'NAME': 'apps.core.password_validation.HaveIBeenPwned'},
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

SESSION_ENGINE = 'qsessions.backends.cached_db'

CACHES = {
    'default': {
        'KEY_PREFIX': 'hnc',
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': env('CACHE_BACKEND', default='redis://localhost:6379/1'),
        'OPTIONS': {
            'SOCKET_TIMEOUT': 5,
            'SOCKET_CONNECT_TIMEOUT': 5,
            'MAX_CONNECTIONS': 1000,
            'SERIALIZER_CLASS': 'redis_cache.serializers.JSONSerializer',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            },
        },
    },
}
# ---------------------------------- Apps ----------------------------------- #
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'qsessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'defender',
]

THIRD_PARTY_APPS = [
    'webpack_loader',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
]

LOCAL_APPS = [
    'apps.core',
    'apps.user',
]

# -------------------- Middlewares & Templates Settings --------------------- #
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'qsessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.core.middlewares.AjaxMessaging',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ROOT_DIR.path('templates')],
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
# User must inform email
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED
# User must inform username during singup
ACCOUNT_USERNAME_REQUIRED = False

# DRF CAPTCHA
GR_CAPTCHA_SECRET_KEY = env('CAPTCHA_SECRET_KEY')

# REST Auth
OLD_PASSWORD_FIELD_ENABLED = True
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'apps.core.api.serializers.UserDetailsSerializer',
}

# Webpack Loader
WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'static/',
        'STATS_FILE': os.path.join(
            str(ROOT_DIR.path('../frontend')), 'webpack-stats.json'
        ),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [],
    }
}

# Django Defender
DEFENDER_LOGIN_FAILURE_LIMIT = 5
DEFENDER_BEHIND_REVERSE_PROXY = True
DEFENDER_DISABLE_USERNAME_LOCKOUT = True
DEFENDER_COOLOFF_TIME = 60 * 60 * 24
DEFENDER_USERNAME_FORM_FIELD = 'email'
DEFENDER_CACHE_PREFIX = 'defender'
DEFENDER_REDIS_NAME = 'default'
DEFENDER_ACCESS_ATTEMPT_EXPIRATION = 24 * 14
# -------------------------- Custom Site Settings --------------------------- #
FRONTEND_SITE_DOMAIN = env("SITE_DOMAIN", default="localhost:8080")
FRONTEND_SITE_NAME = env("SITE_NAME", default="Portal Hack 'n' Cast")
