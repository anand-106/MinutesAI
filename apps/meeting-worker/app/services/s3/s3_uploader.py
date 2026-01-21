from uuid import UUID
import uuid
import boto3
from mypy_boto3_s3 import S3Client
import os
from dotenv import load_dotenv
from app.db.session import SessionLocal
from app.db.models import Meeting,Status

load_dotenv()

s3:S3Client = boto3.client("s3")
bucket = os.getenv("S3_BUCKET")

PART_SIZE = 10 * 1024 * 1024

def multipart_upload_file(
    file_path:str,
    key:str,
    meeting_id:str,
    content_type:str='video/mp4'
    
):
    print(f"Uploading file : {file_path}")
    response = s3.create_multipart_upload(
        Bucket=bucket,
        Key=key,
        ContentType=content_type
    )

    upload_id = response["UploadId"]
    parts = []

    try:
        db = SessionLocal()

        meeting = db.query(Meeting).filter(Meeting.id==meeting_id).first()

        if not meeting:
            raise

        with open(file_path,"rb") as f:

            part_number = 1

            while True:

                chunk = f.read(PART_SIZE)

                if not chunk:
                    break

                result = s3.upload_part(
                    Bucket=bucket,
                    Key=key,
                    UploadId=upload_id,
                    PartNumber=part_number,
                    Body=chunk
                )

                parts.append({
                    "PartNumber":part_number,
                    "ETag":result["ETag"]
                })

                print(f"Uploaded part {part_number}")

                part_number +=1
        s3.complete_multipart_upload(
            Bucket=bucket,
            Key=key,
            UploadId=upload_id,
            MultipartUpload={"Parts":parts}
        )
        meeting.key = key
        meeting.upload_id = upload_id
        meeting.status=Status.finished
        db.commit()

    except Exception:
        s3.abort_multipart_upload(
            Bucket=bucket,
            Key=key,
            UploadId=upload_id
        )
        raise

    finally:
        db.close()