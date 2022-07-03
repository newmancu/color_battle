import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ColorMapConsumer(AsyncJsonWebsocketConsumer):

  async def connect(self):

    await self.accept()

  
  async def disconnect(self, code):

    await self.channel_layer.group_discard(
      self.room_group_name,
      self.channel_name
    )

  async def receive_json(self, data):
    msg = data
    await self.channel_layer.group_send(
      self.room_group_name,
      msg
    )

  async def chat_message(self, event):

    msg = event['message']
    await self.send(text_data=msg)