from .base import *  # noqa

# ------------------------------------------------------------------------
# Site Configuration (TEST)
# ------------------------------------------------------------------------
SITE_NAME = WAGTAIL_SITE_NAME = "DigiDex [TEST]"
SITE_PROTOCOL = "http"
SITE_HOSTNAME = "localhost"  # f'test.{BASE_SITE_HOSTNAME}'

ALLOWED_HOSTS = [SITE_HOSTNAME]
WAGTAILADMIN_BASE_URL = f"{SITE_PROTOCOL}://{SITE_HOSTNAME}"

# ------------------------------------------------------------------------
# Database Configuration (TEST)
# ------------------------------------------------------------------------
# DATABASES['default']['NAME'] = DATABASES['default']['TEST']['NAME']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# ------------------------------------------------------------------------
# Email Configuration (TEST)
# ------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
ACCOUNT_EMAIL_SUBJECT_PREFIX = f"[{SITE_NAME}] "

# ------------------------------------------------------------------------
# Security Configuration (TEST)
# ------------------------------------------------------------------------
SECURE_PROXY_SSL_HEADER = None
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

# ------------------------------------------------------------------------
# Logging Configuration (TEST)
# ------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
    },
}
