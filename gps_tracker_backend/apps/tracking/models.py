from django.db import models
from django.utils import timezone

from apps.devices.models import Device


class Location(models.Model):

    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name="locations",
    )

    lat = models.FloatField()

    lon = models.FloatField()

    battery = models.PositiveSmallIntegerField()

    timestamp = models.DateTimeField(
        default=timezone.now,
    )

    class Meta:
        db_table = "locations"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["device", "-timestamp"]),
        ]

    def __str__(self):
        return f"{self.device.device_id} @ {self.timestamp}"
