from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import websockets.routing

application = ProtocolTypeRouter({
    # WebSocket handler
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websockets.routing.websocket_urlpatterns
        )
    ),
    # Other protocol handlers...
})