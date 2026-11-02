from django.urls import path

from .views import AlertListView, GeofenceListCreateView, GeofenceDetailView

app_name = "alerts"

urlpatterns = [
    path("", AlertListView.as_view(), name="alert-list"),
    path("geofences/<int:child_id>/", GeofenceListCreateView.as_view(), name="geofence-list-create"),
    path("geofences/detail/<int:geofence_id>/", GeofenceDetailView.as_view(), name="geofence-detail"),
]
