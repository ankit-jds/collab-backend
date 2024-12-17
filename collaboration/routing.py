from django.urls import re_path
from collaboration.consumers import *

websocket_urlpatterns = [
    re_path(r"ws/collab/$", CollabConsumer.as_asgi()),
]
