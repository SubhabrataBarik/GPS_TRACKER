import uuid
from datetime import datetime, time, timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.accounts.models import Child


PING_MODES = {
    "live": {"label": "Live", "min_seconds": 10, "max_seconds": 30},
    "normal": {"label": "Normal", "min_seconds": 60, "max_seconds": 120},
    "power_save": {"label": "Power Save", "min_seconds": 300, "max_seconds": 600},
}

PING_MODE_CHOICES = [(key, value["label"]) for key, value in PING_MODES.items()]


class Device(models.Model):

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

    device_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
    )

    api_key = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        db_index=True,
    )

    child = models.OneToOneField(
        Child,
        on_delete=models.CASCADE,
        related_name="device",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
    )

    battery = models.PositiveSmallIntegerField(
        default=100,
    )

    last_seen = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        default=timezone.now,
    )

    class Meta:
        db_table = "devices"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.device_id} → {self.child.name}"


class TrackingSchedule(models.Model):
    """
    Daily window during which a device's ingested pings are accepted.
    Hours selected here drive the estimated daily cost
    (settings.TRACKING_RATE_PER_HOUR per hour).
    """

    device = models.OneToOneField(
        Device,
        on_delete=models.CASCADE,
        related_name="tracking_schedule",
    )

    start_time = models.TimeField(default=time(8, 0))

    end_time = models.TimeField(default=time(20, 0))

    is_active = models.BooleanField(default=True)

    ping_mode = models.CharField(
        max_length=20,
        choices=PING_MODE_CHOICES,
        default="normal",
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tracking_schedules"

    def __str__(self):
        return f"{self.device.device_id} {self.start_time}–{self.end_time}"

    @property
    def min_ping_interval_seconds(self):
        return PING_MODES[self.ping_mode]["min_seconds"]

    @property
    def max_ping_interval_seconds(self):
        return PING_MODES[self.ping_mode]["max_seconds"]

    @property
    def suggested_ping_interval_seconds(self):
        return (self.min_ping_interval_seconds + self.max_ping_interval_seconds) // 2

    @property
    def hours_per_day(self):
        start = datetime.combine(datetime.min, self.start_time)
        end = datetime.combine(datetime.min, self.end_time)

        if end <= start:
            end += timedelta(days=1)

        return round((end - start).total_seconds() / 3600, 2)

    @property
    def estimated_daily_cost(self):
        return round(self.hours_per_day * settings.TRACKING_RATE_PER_HOUR, 2)

    def is_within_window(self, moment=None):
        current = (moment or timezone.localtime()).time()

        if self.start_time == self.end_time:
            return True

        if self.start_time < self.end_time:
            return self.start_time <= current < self.end_time

        return current >= self.start_time or current < self.end_time
