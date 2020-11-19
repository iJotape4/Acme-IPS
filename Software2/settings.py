from pathlib import Path
import os
import dj_database_url
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR,"Soy yooo :D")

MEDIA_ROOT = '<your_path>/media'
MEDIA_URL = 'https://acmeips.herokuapp.com/principal/'

SECRET_KEY = 'cf%_l3)+3(e8vf=bhv3aajl866zeh&1xtaj0zr@9$)!elc@+s-'

DEBUG = True

ALLOWED_HOSTS = ['*']
DATABASES = { 'default' : dj_database_url.config(conn_max_age=600)}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'GestionDeCitas',
    'administrador',
    'tempus_dominus',
    'Informes',
    'qr_code',
    'Autenticacion'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'Software2.urls'
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SETTINGS_PATH, './Software2/plantillas/'),],
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

WSGI_APPLICATION = 'Software2.wsgi.application'


DATABASES = {
 
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd56fi4vrfbi4vr',
        'USER': 'godswojakhehjg',
        'PASSWORD': 'cf4fb13d24a1b659b2ef11704bce40c3a11eb848392acfe706e9183ab77514b2',
        'HOST': 'ec2-54-86-57-171.compute-1.amazonaws.com',
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/Software2/Imgs/'

EMAIL_HOST = 'smtp.googlemail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'acmeprueba2@gmail.com'
EMAIL_HOST_PASSWORD = 'Sistemas312'
EMAIL_USE_TLS = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
    '/static/',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')