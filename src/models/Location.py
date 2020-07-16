from pydantic import BaseModel
from typing import List


class AddressString(BaseModel):
    address: str


class Coordinate(BaseModel):
    latitude: float
    longitude: float


class CoordinateGroup(BaseModel):
    coordinates: List[Coordinate]
