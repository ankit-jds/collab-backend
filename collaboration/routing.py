from django.urls import re_path
from collaboration.consumers import *

websocket_urlpatterns = [
    re_path(r"ws/collab/?$", CollabConsumer.as_asgi()),
    re_path(r"ws/collab/(?P<docid>\w+)/?$", CollabConsumer.as_asgi()),
    re_path(
        r"ws/document/(?P<document_id>\w+)/(?P<username>\w+)/?$",
        DocumentConsumer.as_asgi(),
    ),
    re_path(r"ws/connect/?$", AnonymousUserConsumer.as_asgi()),
    # re_path(r"ws/qrlogin/?$", AuthenticatedConsumerConsumer.as_asgi()),
]
