from pydantic import BaseModel
from src.models.Location import Coordinate
from typing import Any, List


class SingleValuePixel(BaseModel):
    layer: str
    coordinate: Coordinate
    value: Any


class SeriesValuePixel(BaseModel):
    layer: str
    coordinate: Coordinate
    values: List[Any]
