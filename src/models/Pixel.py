from pydantic import BaseModel
from src.models.Location import Coordinate
from typing import Any, List
from pydantic import validator


class SingleValuePixel(BaseModel):
    layer: str
    coordinate: Coordinate
    value: Any

    @validator("value")
    def value_validator(cls, v):
        return float(v)


class SeriesValuePixel(BaseModel):
    layer: str
    coordinate: Coordinate
    values: List[Any]
