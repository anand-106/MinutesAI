import boto3
from botocore.config import Config
from mypy_boto3_s3 import S3Client
from dotenv import load_dotenv
import os

load_dotenv()

s3:S3Client = boto3.client("s3",config=Config(signature_version='s3v4'),region_name=os.getenv("AWS_REGION"))
bucket = os.getenv("S3_BUCKET")

def get_s3_presigned_url(key:str,content_type:str,expire_in:int=3600):
    try:
        return s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={
            "Bucket": bucket,
            "Key": key,
            "ResponseContentType": content_type,
            },
            ExpiresIn=expire_in,
            HttpMethod="GET"
        )
    except Exception:
        raise