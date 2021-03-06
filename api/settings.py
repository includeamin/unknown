from pydantic import BaseSettings


class APISettings(BaseSettings):
    MONGO_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "unknown"
    LAYER_COLLECTION: str = "layers"
    MAX_PAGE: int = 15


class Storage(BaseSettings):
    HOST: str = "localhost:32768"
    ACCESS_KEY: str = "minioadmin"
    SECRET_KEY: str = "minioadmin"
    SECURE: bool = False
    RAW_FILES_BUCKET: str = "raw-files"
    LAYER_BUCKET: str = "unknown"


api_settings = APISettings()
storage_settings = Storage()
