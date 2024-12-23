from django.db import connection

from rest_framework.views import APIView
from rest_framework import status
import traceback

from abstract.response import response_wrapper
from collaboration.models import Document


class DocumentView(APIView):

    @response_wrapper
    def get(self, request, response):
        data = {}
        message = ""
        api_status = status.HTTP_200_OK

        try:
            document_id = request.query_params.get("document_id")
            offset = request.query_params.get("offset", 0)
            limit = request.query_params.get("limit", 10)

            objects = Document.objects.all()

            if document_id:
                objects.filter(id=document_id)

            objects = objects.values("id", "name", "created_on", "updated_on")
            total_count = objects.count()
            objects = objects[offset : offset + limit]

            if document_id:
                # retrieve latest content
                # if pending operations then send pending operations to the client
                # client side will apply all the operations
                document = Document.objects.get(id=document_id)
                data = DocumentUIModel(document=document)
                message = "Document retrieved successfully."

            else:
                table_data = [DocumentUIModel(obj) for obj in objects]
                data = {"table_data": table_data, "total_count": total_count}
                message = "Documents retrieved successfully."

        except Document.DoesNotExist:
            print(traceback.format_exc())
            message = "Document does not exist."
            api_status = status.HTTP_400_BAD_REQUEST

        except:
            print(traceback.format_exc())

        response.data = data
        response.message = message
        response.status = api_status

    @response_wrapper
    def post(self, request, response):
        payload = request.data
        name = request.data.get("document_name", "Untitled document")
        document = Document.objects.create(name=name)
        response.data = DocumentUIModel(document=document)
        response.message = "Document Created successfully."


class DocumentUIModel:
    def __init__(self, document: Document):
        self.id = document.id
        self.name = document.name
        # self.content = document.content
        self.created_on = document.created_on_strf
        self.updated_on = document.updated_on_strf
