from rest_framework import serializers

from .models import Device


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


class DeviceIngestSerializer(serializers.Serializer):

    device_id = serializers.CharField()
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    battery = serializers.IntegerField(min_value=0, max_value=100)
    timestamp = serializers.IntegerField(required=False)
    sos = serializers.BooleanField(default=False)
