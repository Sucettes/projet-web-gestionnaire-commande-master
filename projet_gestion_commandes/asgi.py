"""ASGI config for projet_gestion_commandes project."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet_gestion_commandes.settings')

application = get_asgi_application()
