from django.urls import path

from .views import LocationHistoryView

app_name = "tracking"

urlpatterns = [
    path("<str:device_id>/history/", LocationHistoryView.as_view(), name="location-history"),
]
