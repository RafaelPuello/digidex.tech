from .base import *  # noqa: F403 - imported for gunicorn deployment

DEBUG = False

# Database: Use the test database name defined in the environment
DATABASES['default']['NAME'] = DB_TEST_NAME
DATABASES['default']['USER'] = DB_USERNAME
DATABASES['default']['PASSWORD'] = DB_PASSWORD
DATABASES['default']['HOST'] = DB_HOST
DATABASES['default']['PORT'] = DB_PORT

# Disable caching for tests
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Email: Use a dummy email backend for testing
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Logging: Adjust logging settings to avoid excessive output during testing
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
