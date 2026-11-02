from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication import DeviceAPIKeyAuthentication
from .models import Device
from .serializers import DeviceSerializer, DeviceIngestSerializer


# =========================================================
# DEVICE INGEST VIEW  (called by hardware, not parent app)
# =========================================================

class DeviceIngestView(APIView):

    authentication_classes = [DeviceAPIKeyAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):

        device = request.auth

        if device is None:
            return Response(
                {"error": "X-API-Key header required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = DeviceIngestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if data["device_id"] != device.device_id:
            return Response(
                {"error": "device_id does not match API key."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        device.battery = data["battery"]
        device.last_seen = timezone.now()
        device.save(update_fields=["battery", "last_seen"])

        return Response(
            {
                "status": "ok",
                "device_id": device.device_id,
                "lat": data["lat"],
                "lon": data["lon"],
                "battery": data["battery"],
                "sos": data.get("sos", False),
            },
            status=status.HTTP_200_OK,
        )


# =========================================================
# DEVICE LIST VIEW  (called by parent app)
# =========================================================

class DeviceListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        devices = Device.objects.filter(
            child__parent=request.user,
        ).select_related("child")

        serializer = DeviceSerializer(devices, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# =========================================================
# DEVICE DETAIL VIEW  (called by parent app)
# =========================================================

class DeviceDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, device_id):

        try:
            device = Device.objects.select_related("child").get(
                device_id=device_id,
                child__parent=request.user,
            )
        except Device.DoesNotExist:
            return Response(
                {"error": "Device not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DeviceSerializer(device)
        return Response(serializer.data, status=status.HTTP_200_OK)
