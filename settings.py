"""
Django settings file with IP logging middleware registration.

To use this in your Django project:
1. Import this file or copy the MIDDLEWARE configuration to your project's settings.py
2. Make sure 'ip_tracking' is in your INSTALLED_APPS
3. Run migrations: python manage.py makemigrations && python manage.py migrate
"""

# Example Django settings configuration
# Adjust according to your project structure

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # IP Logging Middleware - Add this line
    'ip_tracking.ip_tracking.middleware.IPLoggingMiddleware',
]

# Make sure 'ip_tracking' is in your INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Add the ip_tracking app
    'ip_tracking',
    # Rate limiting
    'django_ratelimit',
]

# Rate Limiting Configuration
RATELIMIT_USE_CACHE = 'default'
RATELIMIT_ENABLE = True

# Cache configuration for rate limiting (using default cache)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Celery Beat Schedule (for periodic tasks)
CELERY_BEAT_SCHEDULE = {
    'detect-suspicious-ips': {
        'task': 'ip_tracking.ip_tracking.tasks.detect_suspicious_ips',
        'schedule': 3600.0,  # Run every hour (3600 seconds)
    },
}

