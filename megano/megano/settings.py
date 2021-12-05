"""
Django settings for megano project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import django_heroku

from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&dlrv^9&iu@-x)(y$f+z0&mie6!!ok1w@45dg^@39uak(pc^&('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
INTERNAL_IPS = [
    '127.0.0.1'
]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'app_shop',
    'app_cart',
    'app_users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'megano.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'frontend')],
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

WSGI_APPLICATION = 'megano.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'ec2-34-233-214-228.compute-1.amazonaws.com',
        'NAME': 'd4gfg3glnus1ft',
        'USER': 'yersiiozfzoqff',
        'PASSWORD': '2d800537fd5c19c9401fa5ac6fce7b74b75f5777bbbe7aab89cc720bcb68e9ec',
        'PORT': '5432',
    }
}
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

FREE_DELIVERY_PROPERTY_NAME = 'free_price'
CUSTOM_DELIVERY_PROPERTY_NAME = 'delivery_price'
EXPRESS_DELIVERY_PROPERTY_NAME = 'delivery_express_price'
MIN_AMOUNT_TO_FREE_DELIVERY_PROPERTY_NAME = 'min_amount_to_free_delivery'

INITIAL_DELIVERY = {
    CUSTOM_DELIVERY_PROPERTY_NAME: {'name': 'Custom', 'price': 200, 'rules': 'max_cart_price:2000;'},
    EXPRESS_DELIVERY_PROPERTY_NAME: {'name': 'Express', 'price': 500, 'rules': None},
    FREE_DELIVERY_PROPERTY_NAME: {'name': 'Free', 'price': 0, 'rules': 'min_cart_price:2000;'},
}
INITIAL_PAYMENTS = [
    ('online', _('Online cart')),
    ('random_account', _('Online from a random account')),
]
# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "assets")

STATIC_URL = '/assets/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'assets'),
    os.path.join(BASE_DIR, 'frontend'),
    "assets",
    "frontend",

]
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
django_heroku.settings(locals())
CART_SESSION_ID = 'cart'
ORDER_SESSION_ID = 'order'
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"