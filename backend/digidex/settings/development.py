from .base import *  # noqa

DEBUG = True

# ------------------------------------------------------------------------
# Site Configuration (DEV)
# ------------------------------------------------------------------------
SITE_NAME = WAGTAIL_SITE_NAME = "DigiDex"
SITE_PROTOCOL = "http"
SITE_HOSTNAME = "localhost"  # 'dev.digidex.tech'

ALLOWED_HOSTS = [SITE_HOSTNAME]
WAGTAILADMIN_BASE_URL = f"{SITE_PROTOCOL}://{SITE_HOSTNAME}"

# ------------------------------------------------------------------------
# Email Configuration (DEV)
# ------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_SUBJECT_PREFIX = ACCOUNT_EMAIL_SUBJECT_PREFIX = f"[{SITE_NAME}] "

# ------------------------------------------------------------------------
# Security Configuration (DEV)
# ------------------------------------------------------------------------
SECURE_PROXY_SSL_HEADER = None
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

# ------------------------------------------------------------------------
# Logging Configuration (DEV)
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
}
