import os
from django.core.asgi import get_asgi_application

"""
  Next 2 lines must be run before python imports of modules 
  that can use Djnago ORM
"""

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'color_battle.settings')
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from .routers import websocket_urlpatterns
from color_battle.middleware import QueryAuthStack

"""
  check if ProtocolTypeRouter is realy needed (?)
  anwer: Yes, otherwise there could be some 5xx errors
  with OriginValidator
"""

application = ProtocolTypeRouter({
  """
    http field will be automaticaly created,
    but we have already created simple ASGI app
    that's why we directly use 'http' key in dict
  """
  "http": django_asgi_app,
  "websocket": AllowedHostsOriginValidator(
    QueryAuthStack(
      URLRouter(websocket_urlpatterns)
    )
  )
})

# application = AllowedHostsOriginValidator(
#     QueryAuthStack(
#       URLRouter(websocket_urlpatterns)
#       )
#   )
