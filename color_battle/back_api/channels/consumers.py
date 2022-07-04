import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ColorMapConsumer(AsyncJsonWebsocketConsumer):

  async def connect(self):
    await self.accept()

    await self.send_json({
      "message": "Connected!!!!",
      "user": self.scope['user'].has_perm('back_api.worker'),
      "scope": str(type(self.scope))
    })

  
  async def disconnect(self, code):

    await self.send_json({
      "message": "Disconnected"
    })
    print(f'close {code}')
    await self.close()

  async def receive_json(self, data):
    msg = data
    await self.send_json({
      "message": "Received"
    })
