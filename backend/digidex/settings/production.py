import os

from .base import *  # noqa

# ------------------------------------------------------------------------
# Site Configuration (PROD)
# ------------------------------------------------------------------------
SITE_NAME = WAGTAIL_SITE_NAME = "DigiDex"
SITE_PROTOCOL = "https"
SITE_HOSTNAME = "digidex.tech"

ALLOWED_HOSTS = [SITE_HOSTNAME, f"www.{SITE_HOSTNAME}"]
WAGTAILADMIN_BASE_URL = f"{SITE_PROTOCOL}://{SITE_HOSTNAME}"

# ------------------------------------------------------------------------
# Email Configuration (PROD)
# ------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_SUBJECT_PREFIX = ACCOUNT_EMAIL_SUBJECT_PREFIX = f"[{SITE_NAME}] "

# ------------------------------------------------------------------------
# Security Configuration (PROD)
# ------------------------------------------------------------------------
SESSION_COOKIE_SECURE = True

SECURE_HSTS_PRELOAD = True
CSRF_TRUSTED_ORIGINS = os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
CSRF_COOKIE_SECURE = True

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", SITE_PROTOCOL)

DEFAULT_HSTS_SECONDS = 30 * 24 * 60 * 60  # 30 days
SECURE_HSTS_SECONDS = int(
    os.environ.get("SECURE_HSTS_SECONDS", DEFAULT_HSTS_SECONDS)
)  # noqa
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Referrer-policy header settings.
REFERRER_POLICY = os.environ.get(  # noqa
    "SECURE_REFERRER_POLICY", "no-referrer-when-downgrade"
).strip()

# ------------------------------------------------------------------------
# Logging Configuration (PROD)
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

# Wagtail-ntag Configuration (BASE)
NFC_TAG_FILTER_METHOD = 'uid_counter'