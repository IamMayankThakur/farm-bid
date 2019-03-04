from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
#
# channel_routing = [
#     route('websocket.connect', consumers.ws_connect),
#     route('websocket.receive', consumers.ws_receive),
#     route('websocket.disconnect', consumers.ws_disconnect),
# ]