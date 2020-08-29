from pydantic import BaseSettings


class APISettings(BaseSettings):
    MONGO_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "unknown"
    LAYER_COLLECTION: str = "layers"


class Storage(BaseSettings):
    HOST: str = 'localhost:32768'
    ACCESS_KEY: str = 'minioadmin'
    SECRET_KEY: str = 'minioadmin'
    SECURE: bool = False
    RAW_FILES_BUCKET: str = 'raw_files'


api_settings = APISettings()
storage_settings = Storage()
