from django.db import transaction

from rest_framework.response import Response
from rest_framework import status
import jsonpickle
import json
import logging


class CustomResponse:
    data = {}
    message = ""
    status = status.HTTP_200_OK

    def getResponse(self):
        response = {"data": self.data, "message": self.message}
        return Response(
            json.loads(jsonpickle.encode(response, unpicklable=False)),
            self.status,
            content_type="application/json",
        )


def response_wrapper(func=None):
    def decorator(func):
        def warpper_function(*args, **kargs):
            response = CustomResponse()
            try:
                response.status = 200
                with transaction.atomic():
                    func(response=response, *args, **kargs)
            except Exception as e:
                logging.getLogger("django").error(repr(e))
                try:
                    if len(e.args) > 0 and e.args[1] == True:
                        response.message = e.args[0]
                    elif e.args[1] == True:
                        response.message = e.args[0].value
                    else:
                        response.message = "Internal Server Error."
                except Exception as e:
                    response.message = "Internal Server Error."
                    response.status = status.HTTP_500_INTERNAL_SERVER_ERROR

                if response.status == 200:
                    response.status = status.HTTP_500_INTERNAL_SERVER_ERROR
            finally:
                return response.getResponse()

        return warpper_function

    if func is not None:
        return decorator(func)
    return decorator
