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

    async_to_sync(channel_layer.group_send)(
        f"tracking_{device.device_id}",
        {
            "type": "location.update",
            "data": {
                "device_id": device.device_id,
                "lat": lat,
                "lon": lon,
                "battery": battery,
                "sos": sos,
                "timestamp": location.timestamp.isoformat(),
            },
        },
    )

    return location
