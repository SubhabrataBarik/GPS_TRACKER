from django.urls import path

from .views import (
    DeviceIngestView,
    DeviceListView,
    DeviceDetailView,
    TrackingScheduleView,
)

app_name = "devices"

urlpatterns = [
    path("", DeviceListView.as_view(), name="device-list"),
    path("ingest/", DeviceIngestView.as_view(), name="device-ingest"),
    path("<str:device_id>/", DeviceDetailView.as_view(), name="device-detail"),
    path("<str:device_id>/schedule/", TrackingScheduleView.as_view(), name="tracking-schedule"),
]
