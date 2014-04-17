import os

from django.conf import settings

from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
settings.INTERNAL_IPS += ('localhost', '127.0.0.1')
settings.ALLOWED_HOSTS += ['localhost', '127.0.0.1']

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Comment this out to enable postmark email sending.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

