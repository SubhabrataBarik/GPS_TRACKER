from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.devices.models import Device

from .serializers import LocationSerializer


class LocationHistoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, device_id):

        try:
            device = Device.objects.get(
                device_id=device_id,
                child__parent=request.user,
            )
        except Device.DoesNotExist:
            return Response(
                {"error": "Device not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        locations = device.locations.all()[:200]

        serializer = LocationSerializer(locations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
