"""
Django settings for booksmartapp project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from decouple import config
from pathlib import Path
from rest_framework.settings import api_settings
import dj_database_url
# from dj_database_url import parse as dburl
import secrets
from django.conf import settings
from django.conf.urls.static import static
import django.conf.global_settings
# import whitenoise

IS_HEROKU_APP = "DYNO" in os.environ and not "CI" in os.environ
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if not IS_HEROKU_APP:
    TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
elif IS_HEROKU_APP:
    # TEMPLATE_DIR = None
    pass

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECRET_KEY = coonfig('SECRET_KEY')
# DEBUG = config('DEBUG', default=False, cast=bool) 
# SECRET_KEY = os.environ.get('SECRET_KEY')

SECRET_KEY = os.environ.get(
   "DJANGO_SECRET_KEY",
   default=secrets.token_urlsafe(nbytes=64),
)


# SECURITY WARNING: don't run with debug turned on in production!
if IS_HEROKU_APP:
    DEBUG = False
elif not IS_HEROKU_APP:
    DEBUG = True

if IS_HEROKU_APP:
    # ALLOWED_HOSTS = ["booksmartapp-d4d06d34cc80.herokuapp.com"]
    ALLOWED_HOSTS = ["booksmart-app-bd32a8932ff0.herokuapp.com"]
elif not IS_HEROKU_APP:
    ALLOWED_HOSTS = ['127.0.0.1']
else:
    ALLOWED_HOSTS = ['127.0.0.1']


# https://pypi.org/project/django-filter/

INSTALLED_APPS = [
    # 'booksmart.apps.BooksmartConfig',
    # 'accounts.apps.AccountsConfig',
    # 'booksearch.apps.BooksearchConfig',
    'accounts',
    'booksearch',
    'booksmart',
    'browserapi',
    'mainsite',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

     "whitenoise.runserver_nostatic",

    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_filters', 
    'rest_framework_word_filter',

    'rest_framework',
    'rest_auth.registration',
    'rest_framework.authtoken',
    'rest_auth',
 
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'bootstrap4',
    # 'crispy_forms',
    'django_currentuser',

    
    #'crum'
    ]

SITE_ID = 1
# CRISPY_TEMPLATE_PACK = 'uni_form'
# CRISPY_TEMPLATE_PACK = 'bootstrap4'

# SESSION_COOKIE_NAME = "logged-in-user logged-in-sig"
SESSION_COOKIE_SAMESITE = 'None'  # As a string
SESSION_COOKIE_SECURE = True

SESSION_ENGINE= 'django.contrib.sessions.backends.signed_cookies'

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
    'django.middleware.security.SecurityMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# MIDDLEWARE += ['crum.CurrentRequestUserMiddleware',]

X_FRAME_OPTIONS = 'SAMEORIGIN'

ROOT_URLCONF = 'bookmain.urls'
# ROOT_URLCONF = 'booksmartapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # 'DIRS': [BASE_DIR / 'templates'],
        # 'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
            ],
        },
    },
]

# WSGI_APPLICATION = 'bookmain.wsgi.application'
# if IS_HEROKU_APP:
    # WSGI_APPLICATION = 'bookmain.wsgi.application'
# elif not IS_HEROKU_APP:
    # WSGI_APPLICATION = None


# default_dburl = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
# DATABASES = { 'default': config('DATABASE_URL', default=default_dburl, cast=dburl), }

if IS_HEROKU_APP:
    # In production on Heroku the database configuration is derived from the `DATABASE_URL`
    # environment variable by the dj-database-url package. `DATABASE_URL` will be set
    # automatically by Heroku when a database addon is attached to your Heroku app. See:
    # https://devcenter.heroku.com/articles/provisioning-heroku-postgres
    # https://github.com/jazzband/dj-database-url
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            ssl_require=True,
        ),
    }
else:
    # When running locally in development or in CI, a sqlite database file will be used instead
    # to simplify initial setup. Longer term it's recommended to use Postgres locally too.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

REST_FRAMEWORK = {

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        #'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',  
        # 'rest_framework.filters.SearchFilter',
        ],

    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    
    'DEFAULT_CONTENT_NEGOTIATION_CLASS':
    'rest_framework.negotiation.DefaultContentNegotiation',
    # 'DEFAULT_PARSER_CLASSES': [
    #     'rest_framework.parsers.JSONParser',
    #     'rest_framework.parsers.FormParser',
    #     'rest_framework.parsers.MultiPartParser'
    # ],
       
        #'rest_framework_simplejwt.authentication.JWTAuthentication',
    # 'DEFAULT_RENDERER_CLASSES': [
    #     'rest_framework.renderers.BrowsableAPIRenderer',
    # #     'rest_framework.renderers.TemplateHTMLRenderer',
    #     'rest_framework.renderers.JSONRenderer',  
    #  ],
    
    'DEFAULT_PERMISSION_CLASSES': [
        #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        #'rest_framework.permissions.IsAuthenticated',  ### !!!
        'rest_framework.permissions.AllowAny',
     ],
    
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer'
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    # 'TEST_REQUEST_DEFAULT_FORMAT': 'json'
#     ],
#     'DEFAULT_THROTTLE_CLASSES': [
#         'rest_framework.throttling.ScopedRateThrottle',
#     ],
#     'DEFAULT_THROTTLE_RATES': {
#         'cars_app': '50/day',
#         'first_app': '4/day'
#     }


}
# STATICFILES_STORAGE = 'bookmain.storage.S3Storage'

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'accounts.serializer.UserDetailsSerializer'
}

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': 'C:/Users/Python/Desktop/MyApi',
#     }
# }

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


LOGIN_REDIRECT_URL = "/api"
LOGOUT_REDIRECT_URL = "/api" 
REGISTRATION_REDIRECT_URL = "/api"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
# TIME_ZONE = 'Asia/Dubai'
USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# STATICFILES_STORAGE = 'bookmain.storage.S3Storage'
if not IS_HEROKU_APP:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
elif IS_HEROKU_APP:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATIC_URL = "/static/"

# STATIC_ROOT = BASE_DIR / "staticfiles"


# STATICFILES_DIRS = [
#    BASE_DIR/'static'
   # os.path.join(BASE_DIR, "staticfiles"),
#]
# STATICFILES_DIRS = ["staticfiles"]

# MEDIA_URL = '/media/'
# MEDIA_ROOT = '/mymedia/'

if IS_HEROKU_APP:
    # STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
elif not IS_HEROKU_APP:
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'staticfiles'),)  # new

# STATIC_ROOT = "/var/www/booksmartapp/static/css"
# STATIC_DIR=os.path.join(BASE_DIR,'static')
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

WHITENOISE_KEEP_ONLY_HASHED_FILES = True


# AUTH_USER_MODEL = 'bookstore.User'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

AUTH_USER_MODEL = 'accounts.Account'
ACCOUNT_EMAIL_REQUIRED = False


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

if ENVIRONMENT == 'production':
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')



STORAGES = {
    # Enable WhiteNoise's GZip and Brotli compression of static assets:
    # https://whitenoise.readthedocs.io/en/latest/django.html#add-compression-and-caching-support
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# DATE_INPUT_FORMATS = [
#     *django.conf.global_settings.DATE_INPUT_FORMATS,
#     '%m/%d/%Y'
# ]

# USE_L10N = False
# DATE_FORMAT = '%m/%d/%Y'

import django_heroku
django_heroku.settings(locals())