from api.settings import storage_settings
from minio import Minio
from typing import Optional


class Storage:
    def __init__(
        self,
        raw_file: Optional[str] = None,
        new_name: Optional[str] = None,
        layer_id: Optional[str] = None,
    ):
        self.raw: str = raw_file
        self.new_name = new_name
        self._raw_bucket: str = storage_settings.RAW_FILES_BUCKET
        self._minio = Minio(
            endpoint=storage_settings.HOST,
            access_key=storage_settings.ACCESS_KEY,
            secret_key=storage_settings.SECRET_KEY,
            secure=storage_settings.SECURE,
        )
        self._layer_bucket = storage_settings.LAYER_BUCKET
        self._layer_id: str = layer_id

    def layer_file_name(self):
        return f"{self._layer_id}/{self.new_name}"

    def raw_file_path(self):
        return f"{self._raw_bucket}/{self.raw}"

    async def move(self):
        if not self.raw or not self._layer_id or not self.new_name:
            raise Exception("parameters not correct")
        result = self._minio.copy_object(
            bucket_name=self._layer_bucket,
            object_name=self.layer_file_name(),
            object_source=self.raw_file_path(),
        )

    async def delete(self, file_name: str):
        if not self._layer_id:
            raise Exception("layer if not set")
        self._minio.remove_object(self._layer_bucket, f"{self._layer_id}/{file_name}")
