from pydantic import BaseSettings


class APISettings(BaseSettings):
    MONGO_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "unknown"
    LAYER_COLLECTION: str = "layers"


class Storage(BaseSettings):
    HOST: str
    ACCESS_KEY: str
    SECRET_KEY: str
    SECURE: bool
    RAW_FILES_BUCKET: str


api_settings = APISettings()
storage_settings = Storage()
