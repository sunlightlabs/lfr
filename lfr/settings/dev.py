import os

from django.conf import settings

from .base import *

DEBUG = True

SUNLIGHT_API_KEY = os.environ['SUNLIGHT_API_KEY']
INTERNAL_IPS = ['localhost']
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

settings.TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.request',)
