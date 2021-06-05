"""Django settings for projet_gestion_commandes project."""

from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
from mongoengine import connect

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*cwbh+8d!!-r2d5#p$f2*e-=punpu1h2ai=zhy^lpe@^#3bdvf'

DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django_sass',
    'gestion_commandes.apps.GestionCommandesConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'projet_gestion_commandes.urls'

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

WSGI_APPLICATION = 'projet_gestion_commandes.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Base de données
MONGO_DATABASE_NAME = 'GestionCommandesBD'
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
connect(MONGO_DATABASE_NAME, host=MONGO_HOST, port=MONGO_PORT)

STATIC_URL = '/static/'
