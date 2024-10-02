from .base import *  # noqa

# ------------------------------------------------------------------------
# Site Configuration (PROD)
# ------------------------------------------------------------------------
WAGTAIL_SITE_NAME = "DigiDex"
SITE_PROTOCOL = "https"
SITE_HOSTNAME = "digidex.tech"

ALLOWED_HOSTS = [SITE_HOSTNAME, f"www.{SITE_HOSTNAME}"]
WAGTAILADMIN_BASE_URL = f"{SITE_PROTOCOL}://{SITE_HOSTNAME}"

# ------------------------------------------------------------------------
# Email Configuration (PROD)
# ------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = os.getenv("EMAIL_HOST")  # noqa: F405
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")  # noqa: F405
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")  # noqa: F405
EMAIL_PORT = os.getenv("EMAIL_PORT")  # noqa: F405
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")  # noqa: F405

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_SUBJECT_PREFIX = ACCOUNT_EMAIL_SUBJECT_PREFIX = f"[{WAGTAIL_SITE_NAME}] "

# ------------------------------------------------------------------------
# Storage Configuration (PROD)
# ------------------------------------------------------------------------
AWS_S3_FILE_OVERWRITE = False

AWS_ACCESS_KEY_ID = os.getenv("SPACES_ACCESS_KEY")  # noqa: F405
AWS_SECRET_ACCESS_KEY = os.getenv("SPACES_SECRET_KEY")  # noqa: F405
AWS_S3_REGION_NAME = os.getenv("SPACES_REGION_NAME")  # noqa: F405
AWS_S3_ENDPOINT_URL = f'https://{AWS_S3_REGION_NAME}.digitaloceanspaces.com'

AWS_STORAGE_BUCKET_NAME_MEDIA = os.getenv("MEDIA_SPACES_BUCKET_NAME")  # noqa: F405
AWS_STORAGE_BUCKET_NAME_STATIC = os.getenv("STATIC_SPACES_BUCKET_NAME")  # noqa: F405

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
WAGTAIL_REDIRECTS_FILE_STORAGE = "cache"

# ------------------------------------------------------------------------
# Storage-URL Configuration (BASE)
# ------------------------------------------------------------------------
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME_MEDIA}.{AWS_S3_ENDPOINT_URL}/'
STATIC_URL = 'cdn."digidex.tech"/'

# ------------------------------------------------------------------------
# Storage-Staticfiles Configuration (BASE)
# ------------------------------------------------------------------------
STATIC_ROOT = 'static/'
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# ------------------------------------------------------------------------
# Security Configuration (PROD)
# ------------------------------------------------------------------------
SESSION_COOKIE_SECURE = True

SECURE_HSTS_PRELOAD = True
CSRF_TRUSTED_ORIGINS = os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")  # noqa: F405
CSRF_COOKIE_SECURE = True

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", SITE_PROTOCOL)

DEFAULT_HSTS_SECONDS = 30 * 24 * 60 * 60  # 30 days
SECURE_HSTS_SECONDS = int(
    os.environ.get("SECURE_HSTS_SECONDS", DEFAULT_HSTS_SECONDS)  # noqa: F405
)
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Referrer-policy header settings.
REFERRER_POLICY = os.environ.get(  # noqa: F405
    "SECURE_REFERRER_POLICY", "no-referrer-when-downgrade"
).strip()

# ------------------------------------------------------------------------
# Logging Configuration (PROD)
# ------------------------------------------------------------------------
LOG_DIR = os.path.join(PROJECT_DIR, 'logs')  # noqa: F405
if not os.path.exists(LOG_DIR):  # noqa: F405
    os.makedirs(LOG_DIR)  # noqa: F405


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'error.log'),  # noqa: F405
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Wagtail-ntag Configuration (BASE)
NFC_TAG_FILTER_METHOD = 'uid_counter'
