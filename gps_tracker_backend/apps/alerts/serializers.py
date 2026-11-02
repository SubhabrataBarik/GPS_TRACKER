from rest_framework import serializers

from .models import Alert, Geofence


class AlertSerializer(serializers.ModelSerializer):

    child_name = serializers.CharField(source="child.name", read_only=True)

    class Meta:
        model = Alert
        fields = [
            "id",
            "child",
            "child_name",
            "alert_type",
            "lat",
            "lon",
            "message",
            "created_at",
        ]
        read_only_fields = ["id", "child", "child_name", "created_at"]


class GeofenceSerializer(serializers.ModelSerializer):

    child_name = serializers.CharField(source="child.name", read_only=True)

    class Meta:
        model = Geofence
        fields = [
            "id",
            "child",
            "child_name",
            "name",
            "type",
            "lat",
            "lon",
            "radius_meters",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "child", "child_name", "created_at"]
