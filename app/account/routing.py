# your_app/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/upload_progress/', consumers.UploadProgressConsumer.as_asgi()),
    # Add more WebSocket URL patterns as needed
]
