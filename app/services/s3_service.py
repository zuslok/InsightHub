import boto3
from botocore.client import Config
from app.core.config import settings
from uuid import uuid4

s3 = boto3.client(
    "s3",
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
    config=Config(signature_version="s3v4",
                connect_timeout=10,
                read_timeout=60,
                retries={"max_attempts": 5})
)

def upload_bytes_to_s3(data: bytes, filename: str) -> str:
    key = f"{settings.S3_PREFIX}{uuid4()}_{filename}"
    s3.put_object(Bucket=settings.S3_BUCKET, Key=key, Body=data)
    return f"s3://{settings.S3_BUCKET}/{key}"

def read_s3_object(s3_url: str) -> bytes:
    # s3_url: s3://bucket/key
    assert s3_url.startswith("s3://")
    _, _, bucket_and_key = s3_url.partition("s3://") # -> "", "s3://", "bucket/key"
    bucket, _, key = bucket_and_key.partition("/")
    obj = s3.get_object(Bucket=bucket, Key=key)
#     {
#     "Body": <StreamingBody> ,
#     "ContentType": "image/png",
#     "ContentLength": 12345,
#     ...
#    }
    return obj["Body"].read() # -> raw bytes of file.csv