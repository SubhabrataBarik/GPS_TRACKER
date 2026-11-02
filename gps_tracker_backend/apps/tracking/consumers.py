import json

from channels.generic.websocket import AsyncWebsocketConsumer


class TrackingConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.device_id = self.scope["url_route"]["kwargs"]["device_id"]
        self.group_name = f"tracking_{self.device_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def location_update(self, event):

        await self.send(text_data=json.dumps(event["data"]))

    async def sos_alert(self, event):

        await self.send(text_data=json.dumps(event["data"]))
