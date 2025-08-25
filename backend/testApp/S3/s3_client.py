import asyncio
from contextlib import asynccontextmanager
from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from dotenv import load_dotenv, find_dotenv
import os
from fastapi import UploadFile, HTTPException
from typing import Optional
import uuid
from datetime import datetime

load_dotenv(find_dotenv())

access_key = os.getenv("S3_ACCESS_KEY")
secret_key = os.getenv("S3_PRIVATE_KEY")

if not access_key or not secret_key:
    raise ValueError("S3 credentials are not set in environment variables")


class S3Client:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file_from_uploadfile(
        self,
        user_id,
        upload_file: UploadFile,
        folder: Optional[str] = None,
        custom_filename: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> dict:

        try:
            filename = self.generate_image_name(user_id, upload_file.filename)

            if folder:
                folder = folder.strip("/")
                s3_key = f"{folder}/{filename}"
            else:
                s3_key = filename

            content = await upload_file.read()

            final_content_type = (
                content_type
                or upload_file.content_type
                or self._get_content_type(filename)
            )

            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=s3_key,
                    Body=content,
                    ContentType=final_content_type,
                    ACL="public-read",
                )

            file_url = self.get_file_url(s3_key)

            return {
                "success": True,
                "file_url": file_url,
                "filename": filename or upload_file.filename,
                "content_type": final_content_type,
                "size": len(content),
                "folder": folder,
                "s3_key": s3_key,
            }

        except ClientError as e:
            print(f" S3 error: {e}")
            raise HTTPException(500, f"S3 upload error: {str(e)}")
        except Exception as e:
            print(f" Unexpected error: {e}")
            raise HTTPException(500, f"Upload error: {str(e)}")

    def get_file_url(self, s3_key: str) -> str:
        return f"https://099d0323-2777-45e7-b4b3-aa695bb78731.selstorage.ru/{s3_key}"

    def generate_image_name(
        self,
        user_id: int,
        original_filename: str,
        prefix: str = "profile",
    ) -> str:
        user_folder = f"user_{user_id}"
        file_ext = os.path.splitext(original_filename)[-1].lower()
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # unique_id = uuid.uuid4().hex[:8]
        # filename = f"{prefix}_{user_id}_{timestamp}_{unique_id}{file_ext}"
        filename = f"{prefix}_{user_folder}_{user_id}"
        return filename


#     async def delete_file(self, object_name: str):
#         try:
#             async with self.get_client() as client:
#                 await client.delete_object(Bucket=self.bucket_name, Key=object_name)
#                 print(f"File {object_name} deleted from {self.bucket_name}")
#         except ClientError as e:
#             print(f"Error deleting file: {e}")

#     async def get_file(self, object_name: str, destination_path: str):
#         try:
#             async with self.get_client() as client:
#                 response = await client.get_object(Bucket=self.bucket_name, Key=object_name)
#                 data = await response["Body"].read()
#                 with open(destination_path, "wb") as file:
#                     file.write(data)
#                 print(f"File {object_name} downloaded to {destination_path}")
#         except ClientError as e:
#             print(f"Error downloading file: {e}")


s3_client = S3Client(
    access_key=access_key,
    secret_key=secret_key,
    endpoint_url="https://s3.storage.selcloud.ru",
    bucket_name="pet1",
)
