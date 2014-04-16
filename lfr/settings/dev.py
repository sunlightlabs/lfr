import os

from django.conf import settings

from .base import *

DEBUG = True
settings.INTERNAL_IPS += ('localhost', '127.0.0.1')
settings.ALLOWED_HOSTS += ['localhost', '127.0.0.1']

# Comment this out to enable postmark email sending.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# -----------------------------------------------------------------------------
# Sunlight API settings.
SUNLIGHT_API_KEY = os.environ['SUNLIGHT_API_KEY']

# -----------------------------------------------------------------------------
# Postmark API settings.
POSTMARK_API_KEY = os.environ['POSTMARK_API_KEY']
POSTMARK_INBOUND_HASH = os.environ['POSTMARK_INBOUND_HASH']
POSTMARK_INBOUND_HOST = 'inbound.postmarkapp.com'

# True if we set custom domain for the reply-to
# messager rather than inbound.postmarkapp.com. Used in deciding
# whether the reply-to domain is ours or theirs.
# NOTE: an option they suggest is google apps custom forwarding.
# http://support.postmarkapp.com/customer/portal/articles/304511-configuring-a-custom-email-address-forward-with-gmail
POSTMARK_MX_FORWARDING_ENABLED = False

# Postmark SMTP settings
EMAIL_HOST = 'smtp.postmarkapp.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = POSTMARK_API_KEY
EMAIL_HOST_PASSWORD = POSTMARK_API_KEY
EMAIL_USE_TLS = True

EARWIG_URL = 'http://ec2-54-237-85-120.compute-1.amazonaws.com'