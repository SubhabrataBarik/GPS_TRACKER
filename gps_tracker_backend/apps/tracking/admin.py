from django.contrib import admin

from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):

    list_display = ("device", "lat", "lon", "battery", "timestamp")

    list_filter = ("timestamp",)

    search_fields = ("device__device_id",)

    readonly_fields = ("timestamp",)
