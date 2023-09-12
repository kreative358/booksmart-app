import os, environ
from rest_framework.settings import api_settings
import dj_database_url
import secrets
from django.conf import settings
from django.conf.urls.static import static
import django.conf.global_settings
from decouple import config
import django_heroku
from pathlib import Path

# env = environ.Env(
#     # set casting, default value
#     # DEBUG=(bool, True)
#     DEBUG=(bool, True)
# )

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# BOOKMAIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = env('SECRET_KEY', default='S#perS3crEt_007')
# SECRET_KEY = env('SECRET_KEY')
# SECRET_KEY = os.environ.get(
#    "DJANGO_SECRET_KEY",
#    default=secrets.token_urlsafe(nbytes=64),
# )
SECRET_KEY = os.environ.get('SECRET_KEY')

IS_HEROKU_APP = "DYNO" in os.environ and not "CI" in os.environ
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = env('DEBUG')

# if IS_HEROKU_APP or ENVIRONMENT == 'production':
if IS_HEROKU_APP:
    # DEBUG = env('DEBUG')
    DEBUG = True
    # CSRF_TRUSTED_ORIGINS = ['http://localhost:80', 'http://127.0.0.1', 'https://' + 'booksmart-app-bd32a8932ff0.herokuapp.com']
    ALLOWED_HOSTS = ["booksmart-app-bd32a8932ff0.herokuapp.com"]
    CSRF_TRUSTED_ORIGINS = ['https://' + 'booksmart-app-bd32a8932ff0.herokuapp.com']
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    

    # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    # STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
# else:
elif not IS_HEROKU_APP and ENVIRONMENT == 'production':
    pass
# elif ENVIRONMENT == 'development':
elif ENVIRONMENT != 'production':
    DEBUG = True
    CSRF_TRUSTED_ORIGINS = ['http://localhost:80', 'http://127.0.0.1']
    ALLOWED_HOSTS = ['127.0.0.1']
    # 
    # CSRF_TRUSTED_ORIGINS = ['http://localhost:80', 'http://127.0.0.1']
    # STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    # DEBUG = env('DEBUG')

# Assets Management
# ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets') 

# load production server from .env
# ALLOWED_HOSTS        = ['localhost', 'localhost:80', '127.0.0.1', '.herokuapp.com', env('SERVER', default='127.0.0.1') ]
# ALLOWED_HOSTS = ["booksmart-app-bd32a8932ff0.herokuapp.com"]
# CSRF_TRUSTED_ORIGINS = ['http://localhost:80', 'http://127.0.0.1', 'https://' + env('SERVER', default='127.0.0.1') ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',

    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
 
    'rest_framework',
    'django_filters', 
    'rest_framework_word_filter',

    'rest_auth.registration',
    'rest_framework.authtoken',
    'rest_auth',
 
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'bootstrap4',
    # 'crispy_forms',

    'accounts',
    'booksearch',
    'booksmart',
    'browserapi',
    'mainsite',
    'django_currentuser',
    # "drf_recaptcha",
    #'crum'
]

SITE_ID = 1
# SESSION_COOKIE_NAME = "logged-in-user logged-in-sig"
# SESSION_COOKIE_SAMESITE = 'None'  # As a string
# SESSION_COOKIE_SECURE = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django_session_timeout.middleware.SessionTimeoutMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
]

SESSION_EXPIRE_SECONDS = 7200
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_TIMEOUT_REDIRECT = '/'

X_FRAME_OPTIONS = 'SAMEORIGIN'

ROOT_URLCONF = 'bookmain.urls'
# LOGIN_REDIRECT_URL = "index"  # Route defined in mainsite/urls.py
# LOGOUT_REDIRECT_URL = "index"  # Route defined in mainsite/urls.py

AUTH_USER_MODEL = 'accounts.Account'
ACCOUNT_EMAIL_REQUIRED = False
LOGIN_REDIRECT_URL = "/api"
LOGOUT_REDIRECT_URL = "/api" 
REGISTRATION_REDIRECT_URL = "/api"
LOGIN_URL = '/accounts-app/login'

# TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates') # ROOT dir for templates
# TEMPLATE_DIR BASE_DIR / "templates"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                'django.template.context_processors.i18n',
                # 'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
            ],
        },
    },
]

WSGI_APPLICATION = 'bookmain.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases



if IS_HEROKU_APP:
    # heroku addons:create heroku-postgresql:mini
    # db_from_env = dj_database_url.config(conn_max_age=500)
    # DATABASES['default'].update(db_from_env)
    # DATABASES['default'].update(dj_database_url.config(conn_max_age=500, ssl_require=True))
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        ),
    }

# elif os.environ.get('DB_ENGINE') and os.environ.get('DB_ENGINE') == "mysql":
#     DATABASES = { 
#       'default': {
#         'ENGINE'  : 'django.db.backends.mysql', 
#         'NAME'    : os.getenv('DB_NAME'     , 'booksmartappseed_db'),
#         'USER'    : os.getenv('DB_USERNAME' , 'booksmartappseed_db_usr'),
#         'PASSWORD': os.getenv('DB_PASS'     , 'pass'),
#         'HOST'    : os.getenv('DB_HOST'     , 'localhost'),
#         'PORT'    : os.getenv('DB_PORT'     , 3306),
#         }, 
#     }
# else:
elif ENVIRONMENT == 'development':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATIC_ROOT =  BASE_DIR / 'staticfiles'

# STATIC_TMP = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# os.makedirs(STATIC_TMP, exist_ok=True)
# os.makedirs(STATIC_ROOT, exist_ok=True)


# STATIC_URL = '/static/'
# STATIC_URL = 'static/'
# STATIC_ROOT =  os.path.join(BASE_DIR, 'staticfiles')

# STATIC_ROOT = [
#     # 'staticfiles',
#     # BASE_DIR / 'staticfiles',
#     os.path.join(BASE_DIR, 'staticfiles')
#     # os.path.join(BASE_DIR, "static")
#     ]

# Extra places for collectstatic to find static files.
# STATICFILES_DIRS = [
#     # '/static',
#     # BASE_DIR / 'static',
#     os.path.join(BASE_DIR, 'static'),
# ]

# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles'),]
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]

if IS_HEROKU_APP:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    # STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    # STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles'),]
    # STATICFILES_DIRS = [BASE_DIR / "static_build"]
    # STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles'),]
    # STATICFILES_DIRS = ['staticfiles']
    # WHITENOISE_KEEP_ONLY_HASHED_FILES = True
    # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    # STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    # django_heroku.settings(locals())
#     STORAGES = {
#     # Enable WhiteNoise's GZip and Brotli compression of static assets:
#     # https://whitenoise.readthedocs.io/en/latest/django.html#add-compression-and-caching-support
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }
    WHITENOISE_KEEP_ONLY_HASHED_FILES = True
elif ENVIRONMENT == 'development':
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    # STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]

MEDIA_URL = '/media/'
# MEDIA_ROOT = 'media'
# MEDIA_ROOT = 'mediafiles'
MEDIA_ROOT = [  
    os.path.join(BASE_DIR, 'mediafiles')    
    ]


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# 

# EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# import django_heroku
# django_heroku.settings(locals())

# if IS_HEROKU_APP:
#     # https://www.youtube.com/watch?v=ltHkALMK39c
#     # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#     # import django_heroku
#     # django_heroku.settings(locals())
#     pass

# 

# DRF_RECAPTCHA_SECRET_KEY = '6Le3IP4nAAAAAH5J3uPYy4BPPEsS55k0RwCaYxeY'
# https://www.youtube.com/watch?v=ltHkALMK39c
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Emailing settings
# https://www.youtube.com/watch?v=wB1qOExDsYY

if IS_HEROKU_APP and ENVIRONMENT == 'production':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'booksmartapp358@gmail.com'
    EMAIL_FROM = 'booksmartapp358@gmail.com'
    EMAIL_HOST_PASSWORD = 'ikzliaiijzdvbqlq'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

    DEFAULT_FROM_EMAIL = 'booksmartapp358@gmail.com'
    SERVER_EMAIL = 'booksmartapp358@gmail.com'

    # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    # EMAIL_HOST = 'smtp.sendgrid.com'
    # EMAIL_HOST_USER = 'apikey'
    # EMAIL_HOST_PASSWORD = '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'
    # EMAIL_PORT = 587
    # EMAIL_USE_TLS = True

    # PASSWORD_RESET_TIMEOUT = 14400
# elif ENVIRONMENT == 'development':
#     EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# elif DEBUG:
elif ENVIRONMENT == 'development':
    
    # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'booksmartapp358@gmail.com'
    EMAIL_FROM = 'booksmartapp358@gmail.com'
    EMAIL_HOST_PASSWORD = 'ikzliaiijzdvbqlq'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

    # DEFAULT_FROM_EMAIL = 'booksmartapp358@gmail.com'
    # SERVER_EMAIL = 'booksmartapp358@gmail.com'
    # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # During development only

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'