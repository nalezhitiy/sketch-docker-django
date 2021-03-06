"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'ZOvGvCaYTWKWaO')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv('DJANGO_DEBUG', 'False').upper() == 'TRUE' else False

ALLOWED_HOSTS = ['*']

DATA_UPLOAD_MAX_MEMORY_SIZE = 1048576 * 6  # 6MB

# Application definition
BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
    'project',
]
INSTALLED_APPS = BASE_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'project.middleware.SessionLogMiddleware'

]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('APP_DB_NAME'),
        'USER': os.environ.get('APP_DB_USER'),
        'PASSWORD': os.environ.get('APP_DB_PASSWORD'),
        'HOST': os.environ.get('APP_DB_HOST'),
        'PORT': os.environ.get('APP_DB_PORT'),
        'TEST': {
            'NAME': 'test_{}'.format(os.environ.get('APP_DB_NAME')),
        },
    }
}

if os.environ.get('APP_DB_SSL', 'False').upper() == 'TRUE':
    DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_ALLOW_ALL_ORIGINS = False


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] [%(levelname)s] %(message)s'
        },
        'standard': {
            'format': '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)s - %(funcName)s()] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG'
    },
    'loggers': {
        'project': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'propagate': False
        },
    },
}


# Celery application definition
# http://docs.celeryproject.org/en/v4.0.2/userguide/configuration.html
CELERY_BROKER_URL = os.environ.get('APP_CELERY_BROKER_URL')
CELERY_IGNORE_RESULT = True
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Kiev'
CELERY_ENABLE_REMOTE_CONTROL = False
CELERY_SEND_EVENTS = False

CELERY_TASK_ACKS_LATE = True
CELERY_ACKS_LATE = True
CELERYD_PREFETCH_MULTIPLIER = 1

CELERYD_HIJACK_ROOT_LOGGER = False

