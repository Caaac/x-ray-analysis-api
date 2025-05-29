import json

from typing import Annotated, Optional
from src.schemas.xray import SXray
from src.aws.client import s3_client

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
      validation = SXray(**json_data)
      
      image = xray_image.file
      image_name = xray_image.filename
      
      with open(f"{image_name}", "wb") as f:
        f.write(image.read())
      
      print(validation, '\n\n')
      
      print(xray_image)

      print(type(s3_client))
      
      await s3_client.upload_file("/Users/admin/Dev/projects/x-ray-analysis/api/src/test.txt")

      return {"message": "success"}
    except Exception as e:
      raise HTTPException(status_code=400, detail=str(e))
    
