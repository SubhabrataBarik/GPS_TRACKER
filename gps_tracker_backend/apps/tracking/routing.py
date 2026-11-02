from django.urls import path

from .consumers import TrackingConsumer

websocket_urlpatterns = [
    path("ws/tracking/<str:device_id>/", TrackingConsumer.as_asgi()),
]
