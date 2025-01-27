import json
import qrcode
from io import BytesIO
import base64

import qrcode.constants


def make_qr_code(data={"device_id": "self.device_id"}):

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    if type(data) == dict:
        data = json.dumps(data)
    elif type(data) == str:
        data = data
    else:
        return ""

    qr.add_data(data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")

    buffered = BytesIO()
    qr_image.save(buffered)

    qr_image_bytes = buffered.getvalue()

    qr_image_base64 = base64.b64encode(qr_image_bytes).decode("utf-8")
    qr_code_url = f"data:image/png;base64,{qr_image_base64}"

    return qr_code_url
