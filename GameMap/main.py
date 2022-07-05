import os
import pickle

from fastapi import FastAPI, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from utils import schemas
from utils.ColorMap import ColorMap 

settings = {
  'SIZE': tuple(map(int, os.environ.get('MAP_SIZE', '128,128').split(','))),
  'STATIC_ROOT': os.environ.get('STATIC_ROOT', '/usr/src/GameMap/staticfiles'),
  'STATIC_URL': os.environ.get('STATIC_URL', '/static')
}

app = FastAPI()
app.mount(
  settings['STATIC_URL'],
  StaticFiles(directory=settings['STATIC_ROOT']),
  name='static'
)

color_map = ColorMap(settings['SIZE'], settings['STATIC_ROOT'])


@app.post("/set_color")
async def set_color(item: schemas.Item):
  global color_map
  await color_map.set_color(item)
  return JSONResponse(content={}, status_code=status.HTTP_201_CREATED)

@app.post("/save")
async def set_color():
  global color_map
  fp = schemas.FilePath(file_path=await color_map.save())
  fp.file_path = os.path.join(settings['STATIC_URL'], fp.file_path)
  return JSONResponse(content=fp.dict(),status_code=status.HTTP_201_CREATED)

@app.post("/load")
async def set_color(fp: schemas.FilePath):
  global color_map
  await color_map.load(fp)
  return JSONResponse(content={}, status_code=status.HTTP_201_CREATED)

@app.get('/get_img')
async def get_img():
  global color_map
  _map = color_map.img_field
  return JSONResponse(content={'map':str(pickle.dumps(_map))}, status_code=status.HTTP_200_OK)