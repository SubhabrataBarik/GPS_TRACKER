import uuid
from django.db import models
from django.utils import timezone

from apps.accounts.models import Child


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
