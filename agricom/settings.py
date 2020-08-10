import dj_database_url
import dotenv
import os
import django_heroku

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
	dotenv.load_dotenv(dotenv_file)

GDAL_LIBRARY_PATH=os.environ.get('GDAL_LIBRARY_PATH')
SECRET_KEY = '9g80!d_un#x&jw=%h4##8*-lb0s4d0%fb1gt2qt-^$j5o+&u9k'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
   'leaflet',
    'reporter'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'agricom.urls'

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

WSGI_APPLICATION = 'agricom.wsgi.application'

DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)

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
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

#LEAFLET_CONFIG = {
#    'DEFAULT_CENTER': (-.023, 36.87),
#    'DEFAULT_ZOOM': 5,
#    'MAX_ZOOM': 20,
#    'MIN_ZOOM':3,
#    'SCALE': 'both',
#    'ATTRIBUTION_PREFIX': 'Inspired by Life in GIS'
#}

django_heroku.settings(locals())
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

options = DATABASES['default'].get('OPTIONS', {})
options.pop('sslmode', None)
