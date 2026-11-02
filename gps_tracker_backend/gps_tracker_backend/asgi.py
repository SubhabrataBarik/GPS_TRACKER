"""
ASGI config for gps_tracker_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from dotenv import load_dotenv
load_dotenv()

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "gps_tracker_backend.settings.development"
)

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

from apps.tracking.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter(websocket_urlpatterns),
})