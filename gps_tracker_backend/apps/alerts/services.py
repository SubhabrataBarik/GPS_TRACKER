from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from utils.geofence import haversine_distance

from .models import Alert, Geofence


def check_geofences(location):

    device = location.device
    child = device.child

    geofences = Geofence.objects.filter(child=child, is_active=True)

    for geofence in geofences:

        distance = haversine_distance(
            location.lat, location.lon, geofence.lat, geofence.lon,
        )
        is_inside = distance <= geofence.radius_meters

        if is_inside == geofence.is_child_inside:
            continue

        alert_type = "geofence_entry" if is_inside else "geofence_exit"
        action = "entered" if is_inside else "left"

        Alert.objects.create(
            child=child,
            alert_type=alert_type,
            lat=location.lat,
            lon=location.lon,
            message=f"{child.name} {action} {geofence.name}",
        )

        geofence.is_child_inside = is_inside
        geofence.save(update_fields=["is_child_inside"])


def create_sos_alert(location):

    device = location.device
    child = device.child

    alert = Alert.objects.create(
        child=child,
        alert_type="sos",
        lat=location.lat,
        lon=location.lon,
        message=f"SOS triggered by {child.name}",
    )

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"tracking_{device.device_id}",
        {
            "type": "sos_alert",
            "data": {
                "type": "sos",
                "device_id": device.device_id,
                "lat": location.lat,
                "lon": location.lon,
                "message": alert.message,
                "timestamp": alert.created_at.isoformat(),
            },
        },
    )

    return alert
