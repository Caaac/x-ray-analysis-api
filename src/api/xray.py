import json

from typing import Annotated, Optional
from src.schemas.xray import Xray

from fastapi import (
  HTTPException, 
  UploadFile, 
  APIRouter, 
  Header, 
  File, 
  Form
)




router = APIRouter()


@router.post("/xray", name="TEST", tags=["xray"])
async def xray(
    json_data: Annotated[str, Form()],
    xray_image: Annotated[UploadFile, File(...)],
  ):
    try:
      json_data = json.loads(json_data)
      validation = Xray(**json_data)
      
      image = xray_image.file
      image_name = xray_image.filename
      
      with open(f"{image_name}", "wb") as f:
        f.write(image.read())
      
      print(validation, '\n\n')
      
      print(xray_image)
      
      

      return {"message": "success"}
    except Exception as e:
      raise HTTPException(status_code=400, detail=str(e))
    
