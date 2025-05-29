from pydantic import BaseModel, HttpUrl

class SXray(BaseModel):
  callback_url: HttpUrl
  
