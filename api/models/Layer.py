from pydantic import BaseModel
from datetime import datetime
from typing import List


class DateRange(BaseModel):
    start: datetime
    end: datetime


class LayerInformation:
    range: DateRange


class Layer(BaseModel):
    information: LayerInformation
    code: str
    name: str
    description: str = None
    create_at: datetime = datetime.now()
    update_at: datetime = None


class LayerInDB(BaseModel):
    id: str
    information: LayerInformation
    code: str
    name: str
    description: str = None
    create_at: datetime
    update_at: datetime = None


class AddLayerModel(BaseModel):
    information: LayerInformation
    code: str
    name: str
    raw_name: str
    description: str = None


class GetAllLayers(BaseModel):
    result: List[LayerInDB]
    page: int
