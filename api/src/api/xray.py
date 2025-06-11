import os
import json
import uuid

from datetime import datetime
from typing import Annotated, Optional
from sqlalchemy import insert

from src.schemas.xray import SXray
from src.aws import s3_client
# from api.src.db.models import XrayImageOrm
from src.db.database import async_session_factory

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
    json_data: Annotated[str, Form()],
    xray_image: Annotated[UploadFile, File(...)],
):
    try:
        json_data = json.loads(json_data)
        validation = SXray(**json_data)

        image = xray_image.file
        image_name = str(uuid.uuid4()) + '__' + xray_image.filename

        now = datetime.now()
        path = os.path.join(
            'upload',
            str(now.year),
            str(now.month),
        )

        result = await s3_client.upload_file_object(image, image_name, path=path)

        aws_pathname = result['path']

        print(validation.callback_url)
        print(type(validation.callback_url))

        # async with async_session_factory() as session:
        #     stmt = insert(XrayImageOrm).values(
        #         url_from=str(validation.callback_url),
        #         image_path=aws_pathname,
        #         type='chest',
        #     )
        #     await session.execute(stmt)
        #     await session.commit()

        return Response(
            content=json.dumps({"status": "success", "result": result}),
            status_code=201
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
