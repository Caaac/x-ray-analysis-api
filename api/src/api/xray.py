import json
import logging

from typing import Annotated, Union
from typing_extensions import Doc

from src.schemas.xray import SRequsetXray
from src.api.dependencies import predict_service, producer_dep

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
    predict_service: predict_service,
    producer_dep: producer_dep
):
    try:
        json_data = json.loads(json_data)
        
        if not isinstance(xray_images, list):
            xray_images = [xray_images]
        
        req = await predict_service.add_with_files(SRequsetXray(**json_data), xray_images, producer_dep)
        
        return Response(
            content=json.dumps({"status": "success", "data": {"request_guid": str(req.guid)}}),
            status_code=201
        )
    except Exception as e:
        logging.exception(e)
        return Response(
            content=json.dumps({"status": "error", "message": str(e)}),
            status_code=400
        )


from src.rabbitmq.producer import producer_connection
from src.utils.http_client import HttpClient
@router.get("/test")
async def ttt():

    http_client = HttpClient()
    r = await http_client.set_headers({"Application": "test"}).post("http://192.168.1.220:8020/test", json={"test": "test"})
    return r

    async with producer_connection as producer:
        await producer.send_message("Hello!")
    return Response(content=json.dumps({"status": "success"}), status_code=201)
