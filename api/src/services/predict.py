import json

from fastapi import UploadFile

from src.schemas.xray import SRequsetXray
from src.schemas.broker import SXrayMessageResponse
from src.utils.repository import AbstractRepository
from src.db.database import async_session_factory
from src.db.models import XRayRequestOrm, FileOrm, XRayFileOrm
from src.services.aws import AWSService
from src.services.brocker import BrokerService


class PredictService:
    def __init__(self, request_repository: AbstractRepository):
        self.request_repository: AbstractRepository = request_repository()

    async def add_with_files(
        self,
        request_data: SRequsetXray,
        xray_images: list[UploadFile],
        producer_dep: BrokerService
    ) -> int:

        if len(set([f.name for f in request_data.files])) != len(request_data.files):
            raise Exception('Duplicate file names')

        async with async_session_factory() as session:
            new_request = XRayRequestOrm(
                callback_url=str(request_data.callback_url),
                xray_files=[]
            )

            for image in xray_images:
                result = await AWSService.upload_file_object(image)
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

            for xfile in new_request.xray_files:
                await producer_dep.send_message(
                    json.dumps({
                        'request_id': new_request.id,
                        'xray_file_id': xfile.id
                    })
                )

            return new_request.id

        raise Exception('Something went wrong')

    @staticmethod
    async def set_predicted_result(request: SXrayMessageResponse):
        # return await self.request_repository.set_predicted_result(request_id, result)
        ...

    # async def get_with_files(self, id: int):
    #     return await self.request_repository.get_with_files(id)
