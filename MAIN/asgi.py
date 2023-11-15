import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MAIN.settings')

from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from app_customer import routing as app_customer__routing

django_asgi_app  = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket":AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter([
                    *app_customer__routing.websocket_urlpatterns,
                ])
            )
        )
})