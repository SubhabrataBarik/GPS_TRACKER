from django.contrib import admin

from .models import Device, TrackingSchedule


@admin.register(TrackingSchedule)
class TrackingScheduleAdmin(admin.ModelAdmin):

    list_display = (
        "device",
        "start_time",
        "end_time",
        "hours_per_day",
        "estimated_daily_cost",
        "ping_mode",
        "is_active",
    )

    list_filter = ("is_active", "ping_mode")

    search_fields = ("device__device_id",)

    readonly_fields = ("updated_at",)


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
