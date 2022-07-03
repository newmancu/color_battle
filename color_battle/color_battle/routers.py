from django.urls import path, include
from back_api.channels import consumers

websocket_urlpatterns = [
  path('ws/colormap', consumers.ColorMapConsumer.as_asgi()), 
]