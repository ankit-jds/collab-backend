from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
import traceback

from collaboration.models import Document


class DocumentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        kwargs = self.scope.get("url_route", {}).get("kwargs", {})
        self.document_id = kwargs.get("document_id")
        self.group_name = f"collab_{self.document_id}"

        document_content = await self.get_document()
        if document_content != False:
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            await self.send(
                text_data=json.dumps(
                    {
                        "message": f"user connected to {self.group_name}",
                        "content": document_content,
                    }
                )
            )
        else:
            await self.close()

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

    @sync_to_async
    def get_document(self):
        # to retrieve latest content of document
        document_id = self.document_id
        try:
            document = Document.objects.get(id=document_id)
            return document.content
            # can implement caching here to avoid fetching content from database
        except Document.DoesNotExist:
            print(traceback.format_exc())
            return False
