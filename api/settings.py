from pydantic import BaseSettings


class APISettings(BaseSettings):
    MONGO_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "unknown"
    LAYER_COLLECTION: str = "layers"


api_settings = APISettings()
