from django.db import connection

from rest_framework.views import APIView
from rest_framework import status
import traceback

from abstract.response import response_wrapper
from abstract.qrcode import make_qr_code
from collaboration.models import Document


class QRCodeView(APIView):

    @response_wrapper
    def get(self, request, response):
        data = {}
        message = ""
        api_status = status.HTTP_200_OK

        try:
            document_id = request.query_params.get("document_id")

            document = Document.objects.get(id=document_id)

            data = make_qr_code(f"http://192.168.1.24:5173/qrlogin?id={document_id}")
            message = "QR Code generated successfully."

        except Document.DoesNotExist:
            print(traceback.format_exc())
            message = "Document does not exist."
            api_status = status.HTTP_400_BAD_REQUEST

        except:
            print(traceback.format_exc())

        response.data = data
        response.message = message
        response.status = api_status


class DocumentUIModel:
    def __init__(self, document: Document):
        self.id = document.id
        self.name = document.name
        # self.content = document.content
        self.created_on = document.created_on_strf
        self.updated_on = document.updated_on_strf
