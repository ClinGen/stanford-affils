"""WSGI config.

For more information on this file, see:
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

# Built-in libraries:
import os

# Third-party dependencies:
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

application = get_wsgi_application()
