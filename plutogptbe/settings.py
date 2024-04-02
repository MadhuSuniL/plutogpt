import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plutogptbe.settings')
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
django.setup()
from channels.security.websocket import AllowedHostsOriginValidator
from plutogptbe.urls import ws_urlpatterns
from Users.ws_auth_middleware import WsAuthMiddleware

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            WsAuthMiddleware(
                URLRouter(ws_urlpatterns)
            )
        ),
    }
)
