import logging
import uuid
from typing import BinaryIO

from minio import Minio
from minio.error import S3Error

from app.core.config import get_settings

logger = logging.getLogger(__name__)

class MinioService:
    def __init__(self):
        self.settings = get_settings()
        self.client = Minio(
            self.settings.minio_url,
            access_key=self.settings.minio_access_key,
            secret_key=self.settings.minio_secret_key,
            secure=False  # Assuming local development over HTTP without SSL
        )
        self.bucket_name = self.settings.minio_bucket_name
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Creates the bucket if it doesn't already exist."""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Created MinIO bucket: {self.bucket_name}")
        except S3Error as e:
            logger.error(f"Error checking/creating MinIO bucket: {e}")

    def upload_audio_file(self, file_data: BinaryIO, file_size: int, content_type: str, original_filename: str) -> str:
        """
        Uploads an audio file and returns the object path in MinIO.
        This will be used by Day 9 API Route.
        """
        # Generate a unique object name to prevent collisions
        extension = original_filename.split('.')[-1] if '.' in original_filename else 'mp3'
        object_name = f"meetings/{uuid.uuid4()}.{extension}"
        
        try:
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=file_data,
                length=file_size,
                content_type=content_type
            )
            logger.info(f"Successfully uploaded {object_name} to MinIO")
            return object_name
        except S3Error as e:
            logger.error(f"Failed to upload file to MinIO: {e}")
            raise

    def get_audio_url(self, object_name: str) -> str:
        """
        Generates a presigned URL valid for temporary frontend playback.
        """
        try:
            url = self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=object_name
            )
            return url
        except S3Error as e:
            logger.error(f"Failed to generate presigned URL for {object_name}: {e}")
            raise

    def get_audio_file_stream(self, object_name: str):
        """
        Retrieves the raw audio stream.
        IMPORTANT FOR DAY 10: WhisperX will use this method to download 
        the audio file from MinIO back into the background worker's RAM for transcription.
        """
        try:
            response = self.client.get_object(self.bucket_name, object_name)
            return response
        except S3Error as e:
            logger.error(f"Failed to get object stream for {object_name}: {e}")
            raise

    def delete_audio_file(self, object_name: str) -> None:
        """
        Deletes the audio file from MinIO bucket to free up storage space.
        """
        try:
            self.client.remove_object(self.bucket_name, object_name)
            logger.info(f"Successfully deleted {object_name} from MinIO")
        except S3Error as e:
            logger.error(f"Failed to delete {object_name} from MinIO: {e}")

# Singleton instance to be used across the app
minio_service = MinioService()
