from pydantic import BaseSettings


class Location(BaseSettings):
    AGENT_NAME: str = "includeamin"


class Path(BaseSettings):
    base_output_dir: str = "./out"


location_settings = Location()
path_settings = Path()
