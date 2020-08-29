from api.settings import storage_settings
from minio import Minio


class Storage:
    def __init__(self, raw_file: str, new_name: str, layer_id: str):
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
        print(self._layer_bucket)
        print(self.raw)
        print(self.layer_file_name())
        result = self._minio.copy_object(
            bucket_name=self._layer_bucket,
            object_name=self.layer_file_name(),
            object_source=self.raw_file_path(),
        )

    def delete(self):
        pass
