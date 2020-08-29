from pydantic import BaseModel
from typing import List
from src.models.Location import Coordinate


class LayerOptionModel(BaseModel):
    layer_id: str
    layer_item_id: str
    code: str


class WebMapRequestModel(BaseModel):
    coordinate: Coordinate
    layer_list: List[LayerOptionModel]
