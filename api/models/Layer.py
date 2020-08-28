from pydantic import BaseModel
from datetime import datetime
from typing import List


class Layer(BaseModel):
    code: str
    name: str
    description: str = None
    create_at: datetime = datetime.now()
    update_at: datetime = None


class LayerInDB(BaseModel):
    id: str
    code: str
    name: str
    description: str = None
    create_at: datetime
    update_at: datetime = None


class AddLayerModel(BaseModel):
    code: str
    name: str
    description: str = None


class GetAllLayers(BaseModel):
    result: List[LayerInDB]
    page: int
