import os

from django.conf import settings

from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
settings.INTERNAL_IPS += ('localhost', '127.0.0.1')
settings.ALLOWED_HOSTS += ['localhost', '127.0.0.1']

# Comment this out to enable postmark email sending.
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

