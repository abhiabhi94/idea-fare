"""
ASGI config for api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
import sys

from django.core.asgi import get_asgi_application

from config.config import project_name

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      '{}.settings'.format(project_name))

application = get_asgi_application()
