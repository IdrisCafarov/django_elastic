from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/upload_logs/', consumers.LogsConsumer.as_asgi()),
    path('ws/mywebsocket/', consumers.PracticeConsumer.as_asgi()),
]