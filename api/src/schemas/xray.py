from pydantic import BaseModel, HttpUrl
from src.db.enums import XRayContext

class SRequsetFiles(BaseModel):
  name: str
  context: XRayContext

class SRequsetXray(BaseModel):
  callback_url: HttpUrl
  files: list[SRequsetFiles] | SRequsetFiles
  
