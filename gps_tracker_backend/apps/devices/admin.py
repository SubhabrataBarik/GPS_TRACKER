from django.contrib import admin

from .models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):

    list_display = (
        "device_id",
        "child",
        "status",
        "battery",
        "last_seen",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "device_id",
        "child__name",
        "child__parent__phone",
    )

    readonly_fields = (
        "api_key",
        "last_seen",
        "created_at",
    )

    autocomplete_fields = ("child",)
