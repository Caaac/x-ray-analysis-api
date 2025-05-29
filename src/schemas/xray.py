from pydantic import BaseModel, HttpUrl

class Xray(BaseModel):
  callback_url: HttpUrl
  
