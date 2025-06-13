import os
import json
import uuid

from sqlalchemy.orm import selectinload
from sqlalchemy import delete, select
from sqlalchemy import text

from datetime import datetime
from typing import Annotated, Optional, Union
from sqlalchemy import insert

from src.schemas.xray import SRequsetXray
from src.aws import s3_client
from src.db.database import async_session_factory
from src.schemas.models import SXRayRequest, SXRayRequestAdd, SXRayRequestRel, SFile
from src.db.models import XRayRequestOrm, FileOrm, XRayFileOrm
from src.db.enums import XRayContext


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
    xray_images: Annotated[Union[list[UploadFile], UploadFile], File(...)],
):
    try:
        json_data = json.loads(json_data)
        validation = SRequsetXray(**json_data)
        
        files = json_data.get('files', [])
        if len(set([f.get('name') for f in files])) != len(files):
            raise HTTPException(status_code=400, detail="Duplicate file names")

        if not isinstance(xray_images, list):
            xray_images = [xray_images]

        async with async_session_factory() as session:
            new_request = XRayRequestOrm(
                callback_url = str(validation.callback_url),
                xray_files = []
            )            
            
            for image in xray_images:
                print('>>>', image)

                # TODO send to s3 
                image_name = str(uuid.uuid4()) + '__' + image.filename

                now = datetime.now()
                path = os.path.join(
                    'upload',
                    str(now.year),
                    str(now.month),
                )

                result = await s3_client.upload_file_object(image.file, image_name, path=path)
                aws_pathname = result['path']

                new_file = FileOrm(
                    file_name=image.filename,
                    file_size=image.size,
                    path=aws_pathname,
                    content_type=image.content_type,
                )

                session.add(new_file)
                await session.flush()
                    
                context = None
                for f in validation.files:
                    if f.name == image.filename:
                        context = f.context
                    
                new_request.xray_files.append(
                    XRayFileOrm(
                        context_type = context,
                        file_id = new_file.id
                    )
                )

            session.add(new_request)
            await session.commit()

        return Response(
            content=json.dumps({"status": "success", "result": []}),
            status_code=201
        )
    except Exception as e:
        print(e)
        # raise HTTPException(
        #     status_code=400,
            # detail=str(e)
        # )
        return Response(
            content=json.dumps({"status": "error", "message": str(e)}),
            status_code=400
        )


@router.get("/test")
async def test():
    async with async_session_factory() as session:

        # req = XRayRequestOrm(
        #     callback_url="https://test.ru",
        # )
        # session.add(req)
        # await session.flush()
        # print(f"{req=}")
        # print(f"{req.id=}")

        query = (
            select(XRayRequestOrm)
            .options(selectinload(XRayRequestOrm.xray_files))
            .where(XRayRequestOrm.id == 2)
        )

        r = await session.execute(query)
        r = r.scalars().first()

        # print('>>>> ', r.to_schema_rel())

        # print('>>>> ', r.__dict__)
        # for f in r.xray_files:
        #     print('>>>> ', f.__dict__)
        # print('>>>> ', SXRayRequestRel.model_validate(r))
        print('>>>> ', r.to_schema_rel())

        return r.to_schema_rel()

        # rs = [SXRayRequest.model_validate(x, from_attributes=True) for x in r]

        # await session.commit()
