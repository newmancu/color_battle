from pydantic import BaseModel

class Item(BaseModel):
  px: int
  py: int
  color: str


class FilePath(BaseModel):
  file_path: str