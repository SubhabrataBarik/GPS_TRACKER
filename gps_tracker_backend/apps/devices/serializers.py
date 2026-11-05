from django.conf import settings

from rest_framework import serializers

from .models import Device, TrackingSchedule, PING_MODES


class DeviceSerializer(serializers.ModelSerializer):

    child_name = serializers.CharField(
        source="child.name",
        read_only=True,
    )

    child_id = serializers.IntegerField(
        source="child.id",
        read_only=True,
    )

    class Meta:
        model = Device
        fields = [
            "id",
            "device_id",
            "api_key",
            "child_id",
            "child_name",
            "status",
            "battery",
            "last_seen",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "api_key",
            "child_id",
            "child_name",
            "last_seen",
            "created_at",
        ]


class TrackingScheduleSerializer(serializers.ModelSerializer):

    hours_per_day = serializers.FloatField(read_only=True)

    estimated_daily_cost = serializers.FloatField(read_only=True)

    rate_per_hour = serializers.SerializerMethodField()

    min_ping_interval_seconds = serializers.IntegerField(read_only=True)

    max_ping_interval_seconds = serializers.IntegerField(read_only=True)

    ping_mode_options = serializers.SerializerMethodField()

    class Meta:
        model = TrackingSchedule
        fields = [
            "start_time",
            "end_time",
            "is_active",
            "ping_mode",
            "min_ping_interval_seconds",
            "max_ping_interval_seconds",
            "ping_mode_options",
            "hours_per_day",
            "estimated_daily_cost",
            "rate_per_hour",
            "updated_at",
        ]
        read_only_fields = ["updated_at"]

    def get_rate_per_hour(self, obj):
        return settings.TRACKING_RATE_PER_HOUR

    def get_ping_mode_options(self, obj):
        return PING_MODES


class DeviceIngestSerializer(serializers.Serializer):

    device_id = serializers.CharField()
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    battery = serializers.IntegerField(min_value=0, max_value=100)
    timestamp = serializers.IntegerField(required=False)
    sos = serializers.BooleanField(default=False)
