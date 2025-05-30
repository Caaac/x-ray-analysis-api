from src.aws.client import S3Client
from src.aws.config import URL, BUCKET, ACCESS_KEY, SECRET_KEY, REGION

s3_client = S3Client(
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    endpoint_url=URL,
    bucket_name=BUCKET,
    region_name=REGION,
)