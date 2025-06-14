import os
import uuid

from datetime import datetime
from fastapi import UploadFile, HTTPException
from typing import Annotated, Optional, Union

from src.schemas.xray import SRequsetXray
from src.utils.repository import AbstractRepository
from src.db.database import async_session_factory
from src.db.models import XRayRequestOrm, FileOrm, XRayFileOrm
from src.aws import s3_client


class RequestService:
    def __init__(self, request_repository: AbstractRepository):
        self.request_repository: AbstractRepository = request_repository()

    async def add_with_files(self, request_data: SRequsetXray, xray_images: list[UploadFile]) -> int:

        if len(set([f.name for f in request_data.files])) != len(request_data.files):
            raise Exception('Duplicate file names')

        async with async_session_factory() as session:
            new_request = XRayRequestOrm(
                callback_url = str(request_data.callback_url),
                xray_files = []
            )

            for image in xray_images:
                print('>>>', image)

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
                for f in request_data.files:
                    if f.name == image.filename:
                        context = f.context

                new_request.xray_files.append(
                    XRayFileOrm(
                        context_type=context,
                        file_id=new_file.id
                    )
                )

            session.add(new_request)
            await session.commit()

            return new_request.id

        raise Exception('Something went wrong')
