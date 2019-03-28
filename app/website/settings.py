"""
Django for website project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/

For the full list of and their values, see
https://docs.djangoproject.com/en/2.1/ref/
"""

import os, yaml
from jaeger_client import Config
from . import database, tracing
from django.core.exceptions import ImproperlyConfigured


def get_from_django_config(key):
    try:
        global django_configs
        value = django_configs[key]
        if value == "True":
            value = True
        elif value == "False":
            value = False
        return value
    except KeyError:
        raise ImproperlyConfigured("Please define Django configuration parameter: " + key)


def initialize_config():
    def wait_for_config_file():
        max_attempts = 60
        for attempt in range(0, max_attempts):
            file = os.getenv("DJANGO_CONFIGURATION_FILE")
            if os.path.isfile(file):
                return
            if attempt == max_attempts:
                raise TimeoutError("Timed out while waiting for config to become available.")
            print("Waiting for " + file + " to become available...")

    self.wait_for_config_file()
    with open(os.getenv("DJANGO_CONFIGURATION_FILE")) as config_file:
        return yaml.loads(config_file.read())


wait_for_database(
    database_host=get_from_django_config('DATABASES')['default']['HOST'],
    database_port=get_from_django_config('DATABASES')['default']['PORT'],
)
django_configs = initialize_config()

for django_config_key in [
        'SECRET_KEY',
        'DEBUG',
        'ALLOWED_HOSTS',
        'ROOT_URLCONF',
        'INSTALLED_APPS',
        'MIDDLEWARE',
        'LANGUAGE_CODE',
        'TIME_ZONE',
        'USE_I18N',
        'USE_L10N',
        'USE_TZ',
        'STATIC_URL',
        'OPENTRACING_TRACE_ALL',
        'OPENTRACING_TRACED_ATTRIBUTES',
        'OPENTRACING_TRACER_CALLABLE',
        'DATABASES',
]:
    locals()[django_config_key] = get_from_django_config(django_config_key)

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

WSGI_APPLICATION = 'website.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/#auth-password-validators

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
