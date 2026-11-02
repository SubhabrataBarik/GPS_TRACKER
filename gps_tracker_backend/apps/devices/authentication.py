from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import Device


class DeviceAPIKeyAuthentication(BaseAuthentication):
    """
    Authenticates hardware devices via X-API-Key header.
    Returns (None, device) so request.user stays unauthenticated
    and request.auth holds the Device instance.
    """

    def authenticate(self, request):
        api_key = request.META.get("HTTP_X_API_KEY")
        if not api_key:
            return None

        try:
            device = Device.objects.select_related("child__parent").get(
                api_key=api_key,
                status="active",
            )
        except (Device.DoesNotExist, Exception):
            raise AuthenticationFailed("Invalid or inactive device API key.")

        return (None, device)

    def authenticate_header(self, request):
        return "X-API-Key"
