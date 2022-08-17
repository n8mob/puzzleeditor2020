"""
WSGI config for magie_online project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

environment = os.environ.get('APP_ENVIRONMENT', default='local')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'magie_online.settings.{environment}')

application = get_wsgi_application()
