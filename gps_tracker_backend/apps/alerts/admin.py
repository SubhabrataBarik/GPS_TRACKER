from django.contrib import admin

from .models import Alert, Geofence


@admin.register(Geofence)
class GeofenceAdmin(admin.ModelAdmin):

    list_display = ("name", "child", "type", "radius_meters", "is_active", "is_child_inside")

    list_filter = ("type", "is_active")

    search_fields = ("name", "child__name")


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):

    list_display = ("alert_type", "child", "message", "created_at")

    list_filter = ("alert_type", "created_at")

    search_fields = ("child__name", "message")

    readonly_fields = ("created_at",)
