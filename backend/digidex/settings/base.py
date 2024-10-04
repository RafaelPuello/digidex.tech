"""
Django settings for digidex project.
"""
import os
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

from dotenv import load_dotenv

load_dotenv()

DEBUG = False

SECRET_KEY = os.getenv('SECRET_KEY')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = os.path.dirname(PROJECT_DIR)

WAGTAIL_SITE_NAME = "DigiDex"

SITE_PROTOCOL = "http"

SITE_HOSTNAME = os.getenv('SITE_HOSTNAME')

ALLOWED_HOSTS = [SITE_HOSTNAME]  # noqa: F405

WAGTAILADMIN_BASE_URL = f"{SITE_PROTOCOL}://{SITE_HOSTNAME}"  # noqa: F405

INSTALLED_APPS = [
    "taggit",

    "accounts",
    "base",
    "ntags",
    "botany",
    "inventory",
    "home",
    "blog",
    "company",
    "support",
    "search",

    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
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

# ------------------------------------------------------------------------
# Web-App Configuration (BASE)
# ------------------------------------------------------------------------
ROOT_URLCONF = "digidex.urls"
WSGI_APPLICATION = "digidex.wsgi.application"

# ------------------------------------------------------------------------
# Database Configuration (BASE)
# ------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USERNAME'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT')
    }
}

# ------------------------------------------------------------------------
# API Configuration (BASE)
# ------------------------------------------------------------------------
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# ------------------------------------------------------------------------
# Django REST Framework (DRF) Configuration (BASE)
# ------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
}

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

# ------------------------------------------------------------------------
# Authentication Configuration (BASE)
# ------------------------------------------------------------------------
AUTH_USER_MODEL = 'accounts.User'
ACCOUNT_ADAPTER = 'accounts.adapter.UserAccountAdapter'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

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

# Authentication-Username Configuration
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

# Authentication-Email Configuration (BASE)
ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_NOTIFICATIONS = True

# Authentication-URL Configuration (BASE)
LOGIN_URL = '/accounts/login/'
SIGNUP_URL = '/accounts/signup/'
LOGOUT_URL = '/accounts/logout/'
LOGIN_REDIRECT_URL = '/'

# ------------------------------------------------------------------------
# Wagtail-Dashboard Configuration (BASE)
# ------------------------------------------------------------------------
WAGTAILADMIN_RECENT_EDITS_LIMIT = 5
WAGTAILADMIN_EXTERNAL_LINK_CONVERSION = 'exact'

WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'wagtail.admin.rich_text.DraftailRichTextArea',
        'OPTIONS': {
            'features': ['h2', 'bold', 'italic', 'link', 'document-link']
        }
    },
    'secondary': {
        'WIDGET': 'some.external.RichTextEditor',
    }
}

# WAGTAIL_DATE_FORMAT = '%d.%m.%Y.'
# WAGTAIL_DATETIME_FORMAT = '%d.%m.%Y. %H:%M'
# WAGTAIL_TIME_FORMAT = '%H:%M'

# ------------------------------------------------------------------------
# Language Configuration (BASE)
# ------------------------------------------------------------------------
LANGUAGES = [
    ('en', _("English (United Kingdom)")),
    ('en-us', _("English (United States)")),
    ('es', _("Spanish (Spain)")),
    ('es-mx', _("Spanish (Mexico)")),
]

LANGUAGE_CODE = "en-us"
USE_L10N = True
USE_I18N = True

# ------------------------------------------------------------------------
# Timezone Configuration (BASE)
# ------------------------------------------------------------------------
TIME_ZONE = "UTC"
USE_TZ = True

# ------------------------------------------------------------------------
# Wagtail-Internationalization Configuration (BASE)
# ------------------------------------------------------------------------
WAGTAIL_I18N_ENABLED = True

WAGTAIL_CONTENT_LANGUAGES = [
    ('en-us', _("English (United States)")),
    ('es-mx', _("Spanish (Mexico)")),
]

# ------------------------------------------------------------------------
# Wagtail-Image Configuration (BASE)
# ------------------------------------------------------------------------
WAGTAILIMAGES_IMAGE_MODEL = 'base.BaseImage'
# WAGTAILIMAGES_IMAGE_FORM_BASE = 'base.forms.ImageBaseForm'
WAGTAILIMAGES_EXTENSIONS = ['gif', 'jpg', 'jpeg', 'png', 'webp']
WAGTAILIMAGES_MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
WAGTAILIMAGES_MAX_IMAGE_PIXELS = 128000000  # 128 megapixels
WAGTAILIMAGES_FEATURE_DETECTION_ENABLED = True
WAGTAILIMAGES_INDEX_PAGE_SIZE = 30
WAGTAILIMAGES_USAGE_PAGE_SIZE = 20
WAGTAILIMAGES_CHOOSER_PAGE_SIZE = 12
# WAGTAILIMAGES_RENDITION_STORAGE = 'my_custom_storage'

# ------------------------------------------------------------------------
# Wagtail-Document Configuration (BASE)
# ------------------------------------------------------------------------
WAGTAILDOCS_DOCUMENT_MODEL = 'base.BaseDocument'
# WAGTAILDOCS_DOCUMENT_FORM_BASE = 'base.forms.DocumentBaseForm'
WAGTAILDOCS_EXTENSIONS = ['pdf', 'docx']
WAGTAILDOCS_SERVE_METHOD = 'redirect'

WAGTAILDOCS_CONTENT_TYPES = {
    'pdf': 'application/pdf',
    'txt': 'text/plain',
}

WAGTAILDOCS_INLINE_CONTENT_TYPES = [
    'application/pdf',
    'text/plain'
]

# ------------------------------------------------------------------------
# Wagtail-Page Configuration (BASE)
# ------------------------------------------------------------------------
TAGGIT_CASE_INSENSITIVE = True

WAGTAILADMIN_COMMENTS_ENABLED = True
WAGTAIL_ALLOW_UNICODE_SLUGS = False
WAGTAIL_AUTO_UPDATE_PREVIEW = True
WAGTAIL_AUTO_UPDATE_PREVIEW_INTERVAL = 500
WAGTAIL_EDITING_SESSION_PING_INTERVAL = 10000
WAGTAILADMIN_UNSAFE_PAGE_DELETION_LIMIT = 20

# ------------------------------------------------------------------------
# Wagtail-Search Configuration (BASE)
# ------------------------------------------------------------------------
WAGTAILSEARCH_HITS_MAX_AGE = 14

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database',  # elasticsearch8
        # 'INDEX': 'myapp'
    }
}

# ------------------------------------------------------------------------
# Wagtail-ntag Configuration (PROD)
# ------------------------------------------------------------------------
NFC_TAG_FILTER_METHOD = 'uid_counter'

NFC_TAGGABLE_MODELS = ['botany.Plant']
try:
    from .local import *  # noqa
except ImportError:
    pass
