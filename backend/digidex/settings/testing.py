from .base import *  # noqa

DEBUG = False

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

MEDIA_URL = '/test-media/'
STATIC_URL = '/stest-tatic/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'test-media')  # noqa: F405
STATIC_ROOT = os.path.join(BASE_DIR, 'test-static')  # noqa: F405

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'staticfiles'),  # noqa: F405
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'level': 'INFO',
        },
    },
}
