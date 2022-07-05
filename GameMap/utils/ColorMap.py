from datetime import datetime
from PIL import Image
from utils import schemas
from asyncio import Lock
import os


class ColorMap:
  file_path: str
  img_field: Image
  lock = Lock()

  def __init__(self, size: tuple, file_root: str) -> None:
    self.file_path = 'map'
    self.file_root = os.path.join(file_root, self.file_path)
    self.img_field = Image.new('RGB', size)

  def __del__(self):
    self.save()

  async def save(self):
    file = f"{self.file_path}_{datetime.now().strftime('%d-%m-%YT%H:%M:%S')}.png"
    fp = os.path.join(self.file_root,  file)
    self.img_field.save(fp, 'PNG')
    return file

  async def load(self, path: schemas.FilePath):
    async with self.lock:
      self.img_field = Image.open(path.file_path, formats='RGB')

  async def set_color(self, item: schemas.Item):
    async with self.lock:
      self.img_field.putpixel((item.px, item.py),self.__to_rgb(item.color))

  def __to_rgb(self, color):
    ps = [color[c:c+2] for c in range(1,len(color), 2)]
    return tuple(map(lambda x: int(x,16), ps))
