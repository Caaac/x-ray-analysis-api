import json

from typing import Annotated, Optional
from src.schemas.xray import SXray
from src.aws import s3_client

from fastapi import (
  Response,
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
      validation = SXray(**json_data)
      
      image = xray_image.file
      image_name = xray_image.filename
      
      await s3_client.upload_file_object(image, image_name)
            
      return Response(
        content=json.dumps({"status": "success"}), 
        status_code=201
      )
    except Exception as e:
      raise HTTPException(status_code=400, detail=str(e))
    
