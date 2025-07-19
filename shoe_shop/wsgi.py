"""
WSGI config for shoe_shop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoe_shop.settings')

application = get_wsgi_application()


# Ensure correct port (for development, replace `run` with this in manage.py):
if "PORT" in os.environ:
    port = int(os.environ["PORT"])
else:
    port = 8080
