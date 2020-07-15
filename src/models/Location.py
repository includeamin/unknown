from pydantic import BaseModel


class AddressString(BaseModel):
    address: str


class Coordinate(BaseModel):
    latitude: float
    longitude: float
