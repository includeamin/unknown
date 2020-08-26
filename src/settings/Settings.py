from pydantic import BaseSettings


class Location(BaseSettings):
    AGENT_NAME: str = "includeamin"


class Path(BaseSettings):
    base_output_dir: str = "./out"


class Storage(BaseSettings):
    aws_access_key_id: str = 'minioadmin'
    aws_secret_access_key: str = 'minioadmin'
    AWS_HTTPS: str = 'NO'
    GDAL_DISABLE_READDIR_ON_OPEN: str = 'YES'
    AWS_VIRTUAL_HOSTING: str = False
    AWS_S3_ENDPOINT = 'localhost:32768'


location_settings = Location()
path_settings = Path()
storage_settings = Storage()
