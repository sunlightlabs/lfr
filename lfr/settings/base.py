"""
Django settings for lfr project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


BASE_DIR = os.path.join(os.path.dirname(__file__), '..', '..')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
SECRET_KEY = os.environ['DJANGO_LFR_SECRET_KEY']

TEMPLATE_DEBUG = DEBUG
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates')
)

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'lfr.urls'

WSGI_APPLICATION = 'lfr.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')

# Project urls.
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
VERIFY_EMAIL_URL = '/verify_email_pending/'
SET_PASSWORD_URL = '/set_password/'

# Custom auth model since we're using email as username.
AUTH_USER_MODEL = 'app.LfrUser'

# -----------------------------------------------------------------------------
# Sunlight API settings.
SUNLIGHT_API_KEY = os.environ['SUNLIGHT_API_KEY']
EARWIG_URL = os.environ['EARWIG_URL']
EARWIG_KEY = os.environ['EARWIG_KEY']
EARWIG_TTL = int(os.environ['EARWIG_TTL'])
EARWIG_DEBUG_PERSON_ID = os.environ['EARWIG_DEBUG_PERSON_ID']

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
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']