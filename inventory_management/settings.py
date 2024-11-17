from pathlib import Path
from decouple import config, Csv
from logging.handlers import RotatingFileHandler

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load SECRET_KEY from environment variables
SECRET_KEY = config('SECRET_KEY')

# Debug mode (default to False for safety)
DEBUG = config('DEBUG', default=False, cast=bool)

# Allowed hosts
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())

# Installed apps
INSTALLED_APPS = [
    'admin_interface',  # Custom admin styling
    'colorfield',       # Required by admin_interface
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inventory',  # app
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL configuration
ROOT_URLCONF = 'inventory_management.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Custom templates directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'inventory_management.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DATABASE_NAME', default='inventory_db'),
        'USER': config('DATABASE_USER', default='root'),
        'PASSWORD': config('DATABASE_PASSWORD', default=''),
        'HOST': config('DATABASE_HOST', default='localhost'),
        'PORT': config('DATABASE_PORT', default='3306', cast=int),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Directory for static files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# django-admin-interface custom theme settings
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        # Detailed formatter for verbose logs
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',  # Use Python's `{}` formatting style
        },
        # Simple formatter for lightweight logs
        'simple': {
            'format': '{levelname}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        # Rotating file handler for detailed logs
        'file_verbose': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': r'C:\Users\Alex\SecureLogs\verbose_debug.log',  # File for detailed logs
            'maxBytes': 5 * 1024 * 1024,  # 5 MB
            'backupCount': 5,  # Keep up to 5 old log files
            'formatter': 'verbose',  # Use the verbose formatter
        },
        # Rotating file handler for simple logs
        'file_simple': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': r'C:\Users\Alex\SecureLogs\simple_debug.log',  # File for simple logs
            'maxBytes': 5 * 1024 * 1024,  # 5 MB
            'backupCount': 5,  # Keep up to 5 old log files
            'formatter': 'simple',  # Use the simple formatter
        },
    },
    'loggers': {
        # Logger for Django logs
        'django': {
            'handlers': ['file_verbose', 'file_simple'],  # Log to both handlers
            'level': 'DEBUG',  # Log all messages DEBUG and above
            'propagate': True,  # Allow logs to propagate to parent loggers
        },
    },
}

# Security settings for production
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True

# Default threshold for low-stock reports
LOW_STOCK_THRESHOLD = 10
