from .base import *  # noqa: F403 - imported for gunicorn deployment

DEBUG = True

ALLOWED_HOSTS += [  # noqa: F405 - imported from base
    'localhost',
    'www.localhost',
]

WAGTAIL_SITE_NAME = "DigiDex [DEV]"

WAGTAILADMIN_BASE_URL = "http://localhost"

SECURE_PROXY_SSL_HEADER = None

SESSION_COOKIE_SECURE = False

CSRF_COOKIE_SECURE = False

SECURE_SSL_REDIRECT = False

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
        'inventorytags': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

try:
    from .local import *  # noqa
except ImportError:
    pass
