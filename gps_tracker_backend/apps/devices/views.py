from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.alerts.services import check_geofences, create_sos_alert
from apps.tracking.utils import broadcast_location

from .authentication import DeviceAPIKeyAuthentication
from .models import Device, TrackingSchedule
from .serializers import DeviceSerializer, DeviceIngestSerializer, TrackingScheduleSerializer


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

        previous_last_seen = device.last_seen

        device.battery = data["battery"]
        device.last_seen = timezone.now()
        device.save(update_fields=["battery", "last_seen"])

        is_sos = data.get("sos", False)

        schedule, _ = TrackingSchedule.objects.get_or_create(device=device)

        # SOS always gets through, even outside the paid tracking window.
        if schedule.is_active and not is_sos and not schedule.is_within_window():
            return Response(
                {
                    "error": "Outside active tracking hours.",
                    "tracking_window": {
                        "start_time": schedule.start_time.strftime("%H:%M"),
                        "end_time": schedule.end_time.strftime("%H:%M"),
                    },
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # SOS also bypasses the ping-mode rate limit — never throttle an emergency signal.
        if not is_sos and previous_last_seen is not None:
            elapsed_seconds = (device.last_seen - previous_last_seen).total_seconds()
            min_interval = schedule.min_ping_interval_seconds

            # 10% grace tolerance for timer/network jitter on the device side.
            if elapsed_seconds < min_interval * 0.9:
                return Response(
                    {
                        "error": "Pinging too frequently for the selected tracking mode.",
                        "ping_mode": schedule.ping_mode,
                        "min_interval_seconds": min_interval,
                        "seconds_since_last_ping": round(elapsed_seconds, 1),
                    },
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )

        location = broadcast_location(
            device=device,
            lat=data["lat"],
            lon=data["lon"],
            battery=data["battery"],
        )

        check_geofences(location)

        if is_sos:
            create_sos_alert(location)

        return Response(
            {
                "status": "ok",
                "device_id": device.device_id,
                "lat": data["lat"],
                "lon": data["lon"],
                "battery": data["battery"],
                "sos": is_sos,
                "ping_mode": schedule.ping_mode,
                "next_ping_in_seconds": schedule.suggested_ping_interval_seconds,
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


# =========================================================
# TRACKING SCHEDULE VIEW  (parent controls daily tracking window)
# =========================================================

class TrackingScheduleView(APIView):

    permission_classes = [IsAuthenticated]

    def get_device(self, device_id, user):
        return Device.objects.get(device_id=device_id, child__parent=user)

    def get(self, request, device_id):

        try:
            device = self.get_device(device_id, request.user)
        except Device.DoesNotExist:
            return Response(
                {"error": "Device not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        schedule, _ = TrackingSchedule.objects.get_or_create(device=device)

        serializer = TrackingScheduleSerializer(schedule)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, device_id):

        try:
            device = self.get_device(device_id, request.user)
        except Device.DoesNotExist:
            return Response(
                {"error": "Device not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        schedule, _ = TrackingSchedule.objects.get_or_create(device=device)

        serializer = TrackingScheduleSerializer(
            schedule,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
