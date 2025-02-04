from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.core.cache import cache
import redis
import json
import traceback

from collaboration.models import Document, Operation


class DocumentConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        kwargs = self.scope.get("url_route", {}).get("kwargs", {})
        self.document_id = kwargs.get("document_id")
        self.username = kwargs.get("username")

        self.group_name = f"collab_{self.document_id}"
        self.online_users_cache_key = f"{self.group_name}__users"

        document_content = await self.get_document()
        if document_content != False:
            await self.add_user_to_cache(self.username)

            await self.channel_layer.group_add(self.group_name, self.channel_name)

            # Notify all users about the new user
            await self.send_online_users()

            await self.accept()
            # await self.send(
            #     text_data=json.dumps(
            #         {
            #             # will pass userid once auth is setup
            #             "message": f"user connected to {self.group_name}",
            #             "content": document_content,
            #         }
            #     )
            # )
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Remove user from the cache (online users)
        await self.remove_user_from_cache(self.username)

        # Notify all users that the user has disconnected
        await self.send_online_users()

        # Remove the user from the WebSocket group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

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

    # Synchronize methods that interact with cache

    async def add_user_to_cache(self, username):
        # Retrieve the current list of online users from the cache
        online_users = await self.get_online_users()

        # Add the new user to the list if they don't exist
        if username not in online_users:
            online_users.append(username)

        await self.set_online_users(online_users)

    async def remove_user_from_cache(self, username):
        # Retrieve the current list of online users from the cache
        online_users = await self.get_online_users()

        # Remove the user from the list if they exist
        if username in online_users:
            online_users.remove(username)

        await self.set_online_users(online_users)

    @sync_to_async
    def get_online_users(self):
        # Retrieve the list of online users from the cache
        cached_data = cache.get(self.online_users_cache_key)

        if cached_data:
            # Convert the JSON string back to a Python list
            return json.loads(cached_data)
        else:
            # Return an empty list if no users are in the cache
            return []

    async def send_online_users(self):
        # Fetch the list of online users from the cache
        online_users = await self.get_online_users()

        # Send the updated list of online users to all WebSocket clients
        await self.channel_layer.group_send(
            self.group_name, {"type": "update_online_users", "users": online_users}
        )

    async def update_online_users(self, event):
        # Receive the online users and send to WebSocket
        online_users = event["users"]
        await self.send(
            text_data=json.dumps({"type": "update_users", "users": online_users})
        )

    @sync_to_async
    def set_online_users(self, online_users):
        # Store list in cache
        cache.set(self.online_users_cache_key, json.dumps(online_users), timeout=600)
