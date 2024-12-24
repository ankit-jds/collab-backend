from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
import traceback

from collaboration.models import Document, Operation


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
                        # will pass userid once auth is setup
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

        # Here message means list of operations/cursor position
        message = data.get("message", False)

        # check for if data has event type or not
        if event_type and message:

            # event_type for the document updates like insert/update will be document_update
            if event_type == "document_update":
                await self.save_operation_to_database(message)

            # assuming data i.e. JSON text_data follows the validations
            # therefore **data
            await self.channel_layer.group_send(
                self.group_name,
                {"sender": self.channel_name, "type": event_type, **data},
            )

    async def document_update(self, event):
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

    @sync_to_async
    def save_operation_to_database(self, data):
        # [
        #     {"operation": "insert", "character": "h", "position": 1, "userid": "23"},
        #     {"operation": "insert", "character": "i", "position": 2, "userid": "23"},
        # ]
        def check_operation_sanity(op: dict):
            # print(op.items())
            pass

        for op in data:
            # print(op, "op")
            check_operation_sanity(op=op)
            Operation.objects.create(
                document_id=self.document_id,
                operation_type=op.get("operation", ""),
                position=op.get("position", ""),
                character=op.get("character", ""),
                # this will be automatically picked by authentication
                user_id=op.get("userid", ""),
            )
