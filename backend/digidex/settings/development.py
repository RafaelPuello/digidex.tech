from .base import *  # noqa

DEBUG = True

WAGTAIL_SITE_NAME += " (DEV)"

# ------------------------------------------------------------------------
# Email Configuration (DEV)
# ------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_SUBJECT_PREFIX = ACCOUNT_EMAIL_SUBJECT_PREFIX = f"[{WAGTAIL_SITE_NAME}] "

# ------------------------------------------------------------------------
# Storage Configuration (DEV)
# ------------------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # noqa: F405

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # noqa: F405

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'staticfiles'),  # noqa: F405
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

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


# Wagtail-ntag Configuration (BASE)
NFC_TAG_FILTER_METHOD = 'uid'
