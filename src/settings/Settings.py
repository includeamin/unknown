from pydantic import BaseSettings


class Location(BaseSettings):
    AGENT_NAME: str = "includeamin"


location_settings = Location()
