from django.db import models
from django.utils import timezone

from apps.accounts.models import Child


class Geofence(models.Model):

    TYPE_CHOICES = [
        ("home", "Home"),
        ("school", "School"),
        ("custom", "Custom"),
    ]

    child = models.ForeignKey(
        Child,
        on_delete=models.CASCADE,
        related_name="geofences",
    )

    name = models.CharField(max_length=255)

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="custom",
    )

    lat = models.FloatField()

    lon = models.FloatField()

    radius_meters = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)

    is_child_inside = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "geofences"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.child.name})"


class Alert(models.Model):

    ALERT_TYPE_CHOICES = [
        ("sos", "SOS"),
        ("geofence_exit", "Geofence Exit"),
        ("geofence_entry", "Geofence Entry"),
    ]

    child = models.ForeignKey(
        Child,
        on_delete=models.CASCADE,
        related_name="alerts",
    )

    alert_type = models.CharField(
        max_length=20,
        choices=ALERT_TYPE_CHOICES,
    )

    lat = models.FloatField()

    lon = models.FloatField()

    message = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        db_table = "alerts"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.alert_type} - {self.child.name}"
