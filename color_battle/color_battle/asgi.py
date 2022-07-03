import os

from django.core.asgi import get_asgi_application
# from channels.auth import login
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.db import database_sync_to_async
from color_battle.routers import websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'color_battle.settings')

# TODO: check if ProtocolTypeRouter realy needed
# TODO: query authMeddleware

# application = ProtocolTypeRouter({
#   "websocket": AllowedHostsOriginValidator(
#     URLRouter(websocket_urlpatterns)
#   )
# })

application = AllowedHostsOriginValidator(
    URLRouter(websocket_urlpatterns)
  )