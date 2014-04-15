import os

from django.conf import settings

from .base import *

DEBUG = True

SUNLIGHT_API_KEY = os.environ['SUNLIGHT_API_KEY']
INTERNAL_IPS = ['localhost', '127.0.0.1']
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

settings.TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.request',)

# -----------------------------------------------------------------------------
# Postmark settings.
# https://postmarkapp.com/sign_up?reload=true
POSTMARK_API_KEY = '1fa09c20-6469-409f-a592-1eaa0792d04a'
POSTMARK_INBOUND_HASH = 'fc35f26a6a30637e036c0cf8ffa46111'
POSTMARK_INBOUND_HOST = 'inbound.postmarkapp.com'

# True if we set yourearwig.com as the domain of the reply-to
# messager rather than inbound.postmarkapp.com. Used in deciding
# whether the reply-to domain is ours or theirs.
# NOTE: an option they suggest is google apps custom forwarding.
# http://support.postmarkapp.com/customer/portal/articles/304511-configuring-a-custom-email-address-forward-with-gmail
POSTMARK_MX_FORWARDING_ENABLED = False

# If running own email host.
EARWIG_INBOUND_EMAIL_HOST = None

EARWIG_URL = 'http://ec2-54-237-85-120.compute-1.amazonaws.com'