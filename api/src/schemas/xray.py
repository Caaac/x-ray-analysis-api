from pydantic import BaseModel, HttpUrl, UUID4
from src.db.enums import XRayContext

class SRequsetFiles(BaseModel):
  name: str
  hms_file_id: int | None
  context: XRayContext

class SRequsetXray(BaseModel):
  callback_url: HttpUrl
  files: list[SRequsetFiles] | SRequsetFiles
  
class SResponceXray(BaseModel):
  guid: UUID4  
