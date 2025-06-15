import json

from typing import Annotated, Union
from typing_extensions import Doc

from src.schemas.xray import SRequsetXray
from src.api.dependencies import request_service, producer_dep

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
    request_service: request_service,
    producer_dep: producer_dep
):
    try:
        json_data = json.loads(json_data)
        
        if not isinstance(xray_images, list):
            xray_images = [xray_images]
        
        req_id = await request_service.add_with_files(SRequsetXray(**json_data), xray_images, producer_dep)

        return Response(
            content=json.dumps({"status": "success", "data": {"request_id": req_id}}),
            status_code=201
        )
    except Exception as e:
        return Response(
            content=json.dumps({"status": "error", "message": str(e)}),
            status_code=400
        )


from src.rabbitmq.producer import producer_connection
@router.get("/test")
async def ttt():

    async with producer_connection as producer:
        await producer.send_message("Hello!")
    
    return Response(content=json.dumps({"status": "success"}), status_code=201)
