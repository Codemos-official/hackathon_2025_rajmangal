from django.urls import re_path
from .consumers import Chatconsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/$',Chatconsumer.as_asgi()),
]