import asyncio
# import aiofiles
from contextlib import asynccontextmanager

from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from botocore.client import Config

from src.aws.config import URL, BUCKET, ACCESS_KEY, SECRET_KEY, REGION

class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
            region_name: str,
    ):
        self.config = {
            "region_name": region_name,
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
            "config": Config(signature_version="s3"),
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(
            self,
            file_path: str,
    ):
        object_name = file_path.split("/")[-1]  # /users/artem/cat.jpg
        try:
            async with self.get_client() as client:
                with open(file_path, "rb") as file:
                    await client.put_object(
                        Bucket=self.bucket_name,
                        Key=object_name,
                        Body=file,
                    )
                print(f"File {object_name} uploaded to {self.bucket_name}")

            # Асинхронное чтение файла
            # async with aiofiles.open(file_path, "rb") as file:
            #     body_data = await file.read()

            # async with self.get_client() as client:
            #     await client.put_object(
            #         Bucket=self.bucket_name,
            #         Key=object_name,
            #         Body=body_data,
            #     )
            #     print(
            #         f"Файл {object_name} успешно загружен в {self.bucket_name}")
        except ClientError as e:
            print(f"Error uploading file: {e}")

    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
                print(f"File {object_name} deleted from {self.bucket_name}")
        except ClientError as e:
            print(f"Error deleting file: {e}")

    async def get_file(self, object_name: str, destination_path: str):
        try:
            async with self.get_client() as client:
                response = await client.get_object(Bucket=self.bucket_name, Key=object_name)
                data = await response["Body"].read()
                with open(destination_path, "wb") as file:
                    file.write(data)
                print(f"File {object_name} downloaded to {destination_path}")
        except ClientError as e:
            print(f"Error downloading file: {e}")


s3_client = S3Client(
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    endpoint_url=URL,
    bucket_name=BUCKET,
    region_name=REGION,
)

async def main():
    # s3_client = S3Client(
    #     access_key=ACCESS_KEY,
    #     secret_key=SECRET_KEY,
    #     endpoint_url=URL,
    #     bucket_name=BUCKET,
    #     region_name=REGION,
    # )

    # await s3_client.upload_file("test.txt")
    # await s3_client.get_file("test.txt", "text_local_file.txt")
    # await s3_client.delete_file("test.txt")
    
    pass


if __name__ == "__main__":
    asyncio.run(main())
