from channels.generic.websocket import AsyncWebsocketConsumer

import json


class CollabConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        kwargs = self.scope.get("url_route", {}).get("kwargs", {})
        self.group_name = f"collab_{kwargs.get('docid','')}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        # assuming text_data is JSON
        data = json.loads(text_data)
        event_type = data.get("type", False)

        # check for if data has event type or not
        if event_type:
            # assuming data i.e. JSON text_data follows the validations
            # therefore **data
            await self.channel_layer.group_send(
                self.group_name,
                {"sender": self.channel_name, "type": event_type, **data},
            )

    async def chat(self, event):
        if event.get("sender", "") != self.channel_name:
            # assuming message is always in JSON format.
            await self.send(text_data=json.dumps(event.get("message")))
