from channels.generic.websocket import AsyncWebsocketConsumer


class CollabConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        return await super().connect()
