"""WSGI config for projet_gestion_commandes project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet_gestion_commandes.settings')

application = get_wsgi_application()
