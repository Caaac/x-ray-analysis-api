import os
import uuid
from datetime import datetime
from fastapi import UploadFile
from src.aws import s3_client


class AWSService:

    @property
    def img_path(self) -> str:
        now = datetime.now()
        return os.path.join(
            'upload',
            str(now.year),
            str(now.month),
            # str(now.day),
        )

    @staticmethod
    async def upload_file_object(image: UploadFile) -> dict:
        service = AWSService()
        image_name = str(uuid.uuid4()) + '__' + image.filename
        return await s3_client.upload_file_object(image.file, image_name, path=service.img_path)
