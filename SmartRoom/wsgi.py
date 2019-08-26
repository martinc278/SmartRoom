"""
WSGI config for SmartRoom project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
from settings import BASE_DIR
import sys
import os

# path = '/path/to/SmartRoom/src'
path = os.path.join(BASE_DIR)
if path not in sys.path:
    sys.path.append(path)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartRoom.settings')

application = get_wsgi_application()
