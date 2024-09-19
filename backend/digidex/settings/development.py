from .base import *  # noqa: F403 - imported for gunicorn deployment

DEBUG = True

# ------------------------------------------------------------------------
# Site Configuration (DEV)
# ------------------------------------------------------------------------
SITE_NAME = WAGTAIL_SITE_NAME = f"{BASE_SITE_NAME} [DEV]"

SITE_SUBDOMAIN = "dev"

# SITE_HOSTNAME = f'{SITE_SUBDOMAIN}.{BASE_SITE_HOSTNAME}'
SITE_HOSTNAME = "localhost"

ALLOWED_HOSTS = [SITE_HOSTNAME]

SITE_PROTOCOL = "http"

WAGTAILADMIN_BASE_URL = f"{SITE_PROTOCOL}://{SITE_HOSTNAME}"

# ------------------------------------------------------------------------
# Database Configuration (DEV)
# ------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DB_NAME = os.getenv('DB_NAME')

DB_USERNAME = os.getenv('DB_USERNAME')

DB_PASSWORD = os.getenv('DB_PASSWORD')

DB_HOST = os.getenv('DB_HOST')

DB_PORT = os.getenv('DB_PORT')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USERNAME,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT
    }
}

# ------------------------------------------------------------------------
# Storage Configuration (DEV)
# ------------------------------------------------------------------------
AWS_ACCESS_KEY_ID = os.getenv("SPACES_ACCESS_KEY")

AWS_SECRET_ACCESS_KEY = os.getenv("SPACES_SECRET_KEY")

AWS_S3_REGION_NAME = os.getenv("SPACES_REGION_NAME")

AWS_S3_ENDPOINT_URL = f'https://{AWS_S3_REGION_NAME}.digitaloceanspaces.com'

AWS_S3_FILE_OVERWRITE = False

AWS_STORAGE_BUCKET_NAME_MEDIA = os.getenv("MEDIA_SPACES_BUCKET_NAME")

AWS_STORAGE_BUCKET_NAME_STATIC = os.getenv("STATIC_SPACES_BUCKET_NAME")

STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
        'OPTIONS': {
            'access_key': AWS_ACCESS_KEY_ID,
            'secret_key': AWS_SECRET_ACCESS_KEY,
            'region_name': AWS_S3_REGION_NAME,
            'bucket_name': AWS_STORAGE_BUCKET_NAME_MEDIA,
            'endpoint_url': AWS_S3_ENDPOINT_URL,
            'default_acl': 'private',
            'querystring_auth': True,
            'file_overwrite': AWS_S3_FILE_OVERWRITE,
            'object_parameters': {
                'CacheControl': 'max-age=86400',
            },
        }
    },
    'staticfiles': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
        'OPTIONS': {
            'access_key': AWS_ACCESS_KEY_ID,
            'secret_key': AWS_SECRET_ACCESS_KEY,
            'region_name': AWS_S3_REGION_NAME,
            'bucket_name': AWS_STORAGE_BUCKET_NAME_STATIC,
            'endpoint_url': AWS_S3_ENDPOINT_URL,
            'default_acl': 'public-read',
            'querystring_auth': False,
            'file_overwrite': AWS_S3_FILE_OVERWRITE,
            'object_parameters': {
                'CacheControl': 'max-age=86400',
            },
        }
    }
}

# WAGTAIL_REDIRECTS_FILE_STORAGE = "cache"

# ------------------------------------------------------------------------
# Storage-URL Configuration (DEV)
# ------------------------------------------------------------------------
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME_MEDIA}.{AWS_S3_ENDPOINT_URL}/'

STATIC_URL = 'cdn.digidex.tech/'

# ------------------------------------------------------------------------
# Storage-Staticfiles Configuration (DEV)
# ------------------------------------------------------------------------
STATIC_ROOT = 'static/'

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# ------------------------------------------------------------------------
# Search Configuration (DEV)
# ------------------------------------------------------------------------
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

# ------------------------------------------------------------------------
# Email Configuration (DEV)
# ------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_SUBJECT_PREFIX = ACCOUNT_EMAIL_SUBJECT_PREFIX = f"[{SITE_NAME}] "

# ------------------------------------------------------------------------
# Language Configuration (DEV)
# ------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"

WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ('en-us', "English (United States)"),
]

WAGTAIL_I18N_ENABLED = True

USE_L10N = True

USE_I18N = True

# ------------------------------------------------------------------------
# Timezone Configuration (DEV)
# ------------------------------------------------------------------------
TIME_ZONE = "UTC"

USE_TZ = True

# ------------------------------------------------------------------------
# Security Configuration (DEV)
# ------------------------------------------------------------------------
SECURE_PROXY_SSL_HEADER = None

SESSION_COOKIE_SECURE = False

CSRF_COOKIE_SECURE = False

SECURE_SSL_REDIRECT = False

# ------------------------------------------------------------------------
# API Configuration (DEV)
# ------------------------------------------------------------------------
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

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

try:
    from .local import *  # noqa
except ImportError:
    pass
