import rasterio

from rasterio.session import AWSSession
from src.settings.Settings import storage_settings


class StorageManagement:
    def __init__(self):
        self.aws = AWSSession(
            aws_access_key_id=storage_settings.aws_access_key_id,
            aws_secret_access_key=storage_settings.aws_secret_access_key,
            endpoint_url=storage_settings.AWS_S3_ENDPOINT)
        self.ENV = rasterio.Env(AWS_HTTPS=storage_settings.AWS_HTTPS,
                                GDAL_DISABLE_READDIR_ON_OPEN=storage_settings.GDAL_DISABLE_READDIR_ON_OPEN,
                                AWS_VIRTUAL_HOSTING=storage_settings.AWS_VIRTUAL_HOSTING,
                                AWS_S3_ENDPOINT=storage_settings.AWS_S3_ENDPOINT, session=self.aws)

    def get_list_of_tiffs(self, base_path: str):
        pass
