from typing import List, AsyncIterator, AsyncGenerator

import rasterio
import boto3
from rasterio.session import AWSSession
from src.settings.Settings import storage_settings
from minio import Minio
import os


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class StorageManagement(metaclass=Singleton):
    def __init__(self):
        self.aws = AWSSession(
            aws_access_key_id=storage_settings.aws_access_key_id,
            aws_secret_access_key=storage_settings.aws_secret_access_key,
            endpoint_url=storage_settings.AWS_S3_ENDPOINT,
        )
        self.ENV = rasterio.Env(
            AWS_HTTPS=storage_settings.AWS_HTTPS,
            GDAL_DISABLE_READDIR_ON_OPEN=storage_settings.GDAL_DISABLE_READDIR_ON_OPEN,
            AWS_VIRTUAL_HOSTING=storage_settings.AWS_VIRTUAL_HOSTING,
            AWS_S3_ENDPOINT=storage_settings.AWS_S3_ENDPOINT,
            session=self.aws,
        )
        self._s3 = boto3.resource("s3", aws_access_key_id=storage_settings.aws_access_key_id,
                                  aws_secret_access_key=storage_settings.aws_secret_access_key,
                                  endpoint_url=f"http{'s' if storage_settings.IS_SECURE else ''}://" + storage_settings.AWS_S3_ENDPOINT,
                                  use_ssl=storage_settings.IS_SECURE
                                  )
        self._layerBaseBucket = storage_settings.LAYER_BASE_BUCKET
        self._minio = Minio(endpoint=storage_settings.AWS_S3_ENDPOINT,
                            access_key=storage_settings.aws_access_key_id,
                            secret_key=storage_settings.aws_secret_access_key,
                            secure=storage_settings.IS_SECURE)

    async def get_list_of_tiffs(self, base_path: str) -> List[str]:
        result = self._minio.list_objects(bucket_name=self._layerBaseBucket, prefix=base_path, recursive=True)
        return [item.object_name for item in result]

    def get_storage_path(self, path) -> str:
        return os.path.join(f"s3://{self._layerBaseBucket}", path)
