from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Location


def broadcast_location(device, lat, lon, battery, sos=False):

    location = Location.objects.create(
        device=device,
        lat=lat,
        lon=lon,
        battery=battery,
    )

    channel_layer = get_channel_layer()
    group_name = f"tracking_{device.device_id}"

    payload = {
        "device_id": device.device_id,
        "lat": lat,
        "lon": lon,
        "battery": battery,
        "timestamp": location.timestamp.isoformat(),
    }

    async_to_sync(channel_layer.group_send)(
        group_name,
        {"type": "location.update", "data": {**payload, "type": "location"}},
    )

    if sos:
        async_to_sync(channel_layer.group_send)(
            group_name,
            {"type": "location.update", "data": {**payload, "type": "sos"}},
        )

    return location
