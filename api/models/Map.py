from pydantic import BaseModel
from typing import List
from src.models.Location import Coordinate


class LayerOptionModel(BaseModel):
    name: str


class WebMapRequestModel(BaseModel):
    coordinate: Coordinate
    layer_list: List[LayerOptionModel]
