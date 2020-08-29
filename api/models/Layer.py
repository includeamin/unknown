from pydantic import BaseModel
from datetime import datetime, date
from typing import List
from pydantic import validator
from fastapi import HTTPException


class DateRange(BaseModel):
    start: datetime
    end: datetime

    @validator("end")
    def end_validator(cls, v, values):
        if not isinstance(v, datetime):
            raise HTTPException(detail="not instance of date", status_code=400)
        if values["start"].date() >= v.date():
            raise HTTPException(
                detail="end should be greater that start", status_code=400
            )
        return v


class Location(BaseModel):
    type: str = "Point"
    coordinates: List[float]


class LayerInformation(BaseModel):
    range: DateRange


class LayerItem(BaseModel):
    information: LayerInformation
    file_name: str = None


class Layer(BaseModel):
    location: Location
    code: str
    name: str
    description: str = None
    create_at: datetime = datetime.now()
    update_at: datetime = None
    layers: List[LayerItem] = []


class LayerInDB(BaseModel):
    id: str
    location: Location
    code: str
    name: str
    description: str = None
    create_at: datetime = datetime.now()
    update_at: datetime = None
    layers: List[LayerItem] = []


class AddLayerModel(BaseModel):
    location: Location
    code: str
    name: str
    description: str = None


class AddNewLayerItem(BaseModel):
    code: str
    information: LayerInformation
    raw_file_name: str


class GetAllLayers(BaseModel):
    result: List[LayerInDB]
    page: int


class ValidLayers(BaseModel):
    code: str
    name: str
    description: str


class ValidLayersNearLocation(BaseModel):
    results: List[ValidLayers]
    page: int = 1
