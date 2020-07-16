from pydantic import BaseModel
from typing import List


class AddressString(BaseModel):
    address: str


class Coordinate(BaseModel):
    latitude: float
    longitude: float


class AddressInformation(BaseModel):
    full_address: str
    coordinate: Coordinate


class CoordinateGroup(BaseModel):
    coordinates: List[Coordinate]
