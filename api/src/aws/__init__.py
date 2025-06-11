from src.aws.client import S3Client
from src.aws.config import settings

s3_client = S3Client(
    access_key=settings.ACCESS_KEY,
    secret_key=settings.SECRET_KEY,
    endpoint_url=settings.URL,
    bucket_name=settings.BUCKET,
    region_name=settings.REGION,
)