from rest_framework.views import APIView
from abstract.response import response_wrapper


class DocumentView(APIView):

    @response_wrapper
    def get(self, request, response):

        response.data = {"dcoument": "here it is"}
        response.message = "Here is your document..."
        pass
