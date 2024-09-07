"""
Django settings for digidex project.
"""
import os
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = os.path.dirname(PROJECT_DIR)

BASE_HOST = "digidex.tech"

ALLOWED_HOSTS = [
    BASE_HOST,
    f"www.{BASE_HOST}",
]

INSTALLED_APPS = [
    "modelcluster",
    "taggit",
    "queryish",

    "base",
    "accounts",
    "home",
    "search",
    "nearfieldcommunication",
    "biodiversity",
    "inventory",
    "assistant",
    "api",

    "wagtail.contrib.settings",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.routable_page",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    'wagtail.api.v2',
    # "wagtail_ai",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework_simplejwt",
    "allauth",
    "allauth.account",
    "allauth.mfa",
    "allauth.headless",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "digidex.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = "digidex.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'defaultdb'),
        'USER': os.getenv('DB_USERNAME'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'TEST': {
            'NAME': os.getenv('TEST_DB_NAME', 'test_defaultdb'),
            'SERIALIZE': False,
        },
    }
}

# Common S3 settings
AWS_ACCESS_KEY_ID = os.getenv("SPACES_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("SPACES_SECRET_KEY")
AWS_S3_REGION_NAME = os.getenv("SPACES_REGION_NAME")
AWS_S3_ENDPOINT_URL = f'https://{AWS_S3_REGION_NAME}.digitaloceanspaces.com'
AWS_S3_FILE_OVERWRITE = False

# Media Files S3 Configuration
AWS_STORAGE_BUCKET_NAME_MEDIA = os.getenv("MEDIA_SPACES_BUCKET_NAME")

# Static Files S3 Configuration
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

MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME_MEDIA}.{AWS_S3_ENDPOINT_URL}/'

STATIC_URL = 'cdn.digidex.tech/'

STATIC_ROOT = 'static/'

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        },
    },
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Internationalization
LANGUAGE_CODE = "en-us"

LANGUAGES = [
    ('en', _("English (United Kingdom)")),
    ('en-us', _("English (United States)")),
    ('es', _("Spanish (Spain)")),
    ('es-mx', _("Spanish (Mexico)")),
]

TIME_ZONE = "UTC"

USE_L10N = True

USE_I18N = True

USE_TZ = True

WAGTAIL_I18N_ENABLED = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
}

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# These are the URLs to be implemented by your single-page application.
HEADLESS_FRONTEND_URLS = {
    "account_confirm_email": "https://digidex.tech/account/verify-email/{key}",
    "account_reset_password_from_key": "https://digidex.tech/account/password/reset/key/{key}",
    "account_signup": "https://digidex.tech/account/signup",
    "account_confirm_email": "https://digidex.tech/account/verify-email/{key}",
    "account_reset_password": "https://digidex.tech/account/password/reset",
    "account_reset_password_from_key": "https://digidex.tech/account/password/reset/key/{key}",
    "account_signup": "https://digidex.tech/account/signup",
}

# HEADLESS_ONLY = True

# allauth settings
AUTH_USER_MODEL = 'accounts.DigiDexUser'

ACCOUNT_ADAPTER = 'accounts.adapter.DigidexAccountAdapter'

ACCOUNT_PRESERVE_USERNAME_CASING = False

ACCOUNT_USERNAME_MIN_LENGTH = 3

ACCOUNT_USERNAME_BLACKLIST = [
    'admin', 'administrator', 'root', 'sysadmin', 'webmaster', 'django-admin',
    'support', 'helpdesk', 'moderator', 'superuser', 'guest',
    'anonymous', 'nobody', 'user', 'null', 'undefined', 'localhost',
    'default', 'public', 'system', 'official', 'security', 'info',
    'contact', 'feedback', 'no-reply', 'noreply', 'api', 'static',
    'assets', 'img', 'css', 'js', 'javascript', 'fonts', 'media',
    'login', 'logout', 'signup', 'register', 'account', 'profile',
    'subscribe', 'unsubscribe', 'activate', 'deactivate', 'configuration',
    'settings', 'preferences', 'billing', 'payment', 'dashboard',
    'auth', 'authentication', 'token', 'oauth', 'sitemap', 'robots.txt',
    'postmaster', 'hostmaster', 'usenet', 'news', 'web', 'www', 'ftp',
    'mail', 'email', 'smtp', 'pop3', 'imap', 'cdn', 'network', 'messages',
    'notification', 'alerts', 'blog', 'forum', 'wiki', 'help', 'search',
    'dev', 'developer', 'cors', 'about', 'privacy', 'legal', 'terms',
    'services', 'document', 'documents', 'download', 'downloads', 'error', 'errors', '403', '404', '500',
    'base', 'company', 'inventory'
    'new', 'all', 'any', 'every', 'site', 'api-key', 'reset', 'change',
    'start', 'stop', 'edit', 'delete', 'remove', 'read', 'write', 'list',
    'create', 'update', 'confirm', 'save', 'load', 'logout', 'signin', 'signout',
    'test', 'testing', 'demo', 'example', 'batch', 'status',
    'django-admin',
]

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3

ACCOUNT_EMAIL_NOTIFICATIONS = True

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_EMAIL_SUBJECT_PREFIX = "[DigiDex] "

ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS = False

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

LOGIN_URL = '/accounts/login/'

SIGNUP_URL = '/accounts/signup/'

LOGOUT_URL = '/accounts/logout/'

LOGIN_REDIRECT_URL = '/'

if "EMAIL_HOST" in os.environ:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = os.getenv("EMAIL_PORT")
    EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Wagtail settings
WAGTAIL_CONTENT_LANGUAGES = [
    ('en', _("English")),
    ('es', _("Spanish")),
]

WAGTAILIMAGES_IMAGE_MODEL = 'base.BaseImage'

WAGTAILIMAGES_EXTENSIONS = ['gif', 'jpg', 'jpeg', 'png', 'webp']

WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

WAGTAIL_ALLOW_UNICODE_SLUGS = False

TAGGIT_CASE_INSENSITIVE = True
