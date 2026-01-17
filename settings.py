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
    'ip_tracking.middleware.IPLoggingMiddleware',
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
]

