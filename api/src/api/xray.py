import json

from typing import Annotated, Union
from typing_extensions import Doc

from src.schemas.xray import SRequsetXray
from src.repositories.request import XRayRequestRepository
from src.services.request import RequestService

from fastapi import (
    Response,
    HTTPException,
    UploadFile,
    APIRouter,
    Header,
    File,
    Form
)

router = APIRouter(prefix="/api/v1", tags=["xray"])


@router.post("/xray", name="TEST")
async def xray(
    json_data: Annotated[str, Form(), Doc(SRequsetXray)],
    xray_images: Annotated[Union[list[UploadFile], UploadFile], File(...)],
):
    try:
        json_data = json.loads(json_data)
        
        if not isinstance(xray_images, list):
            xray_images = [xray_images]
        
        req_id = await RequestService(XRayRequestRepository).add_with_files(SRequsetXray(**json_data), xray_images)

        return Response(
            content=json.dumps({"status": "success", "data": {"request_id": req_id}}),
            status_code=201
        )
    except Exception as e:
        return Response(
            content=json.dumps({"status": "error", "message": str(e)}),
            status_code=400
        )

