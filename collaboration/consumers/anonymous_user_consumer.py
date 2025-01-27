from channels.generic.websocket import AsyncWebsocketConsumer

import json
import uuid
import qrcode
from io import BytesIO
from PIL import Image
import base64

import qrcode.constants


class AnonymousUserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:

            self.device_id = str(uuid.uuid4())
            self.group_name = f"user_{self.device_id}"

            await self.channel_layer.group_add(self.group_name, self.channel_name)

            await self.accept()

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(json.dumps({"device_id": self.device_id}))
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")

            buffered = BytesIO()
            qr_image.save(buffered)

            qr_image_bytes = buffered.getvalue()

            qr_image_base64 = base64.b64encode(qr_image_bytes).decode("utf-8")
            qr_code_url = f"data:image/png;base64,{qr_image_base64}"

            qr_response = {"data": {"qr": qr_code_url}}

            await self.send(text_data=json.dumps(qr_response))
            print("...here...")

        except Exception as ex:
            await self.send(
                text_data=json.dumps(
                    {
                        "error": f"Unexpected Error occured: {str(ex)}",
                    }
                )
            )

    async def receive(self, text_data):
        # assuming text_data is JSON
        data = json.loads(text_data)
        event_type = data.get("type", False)

        # check for if data has event type or not
        if event_type:
            await self.request_qr_code()
