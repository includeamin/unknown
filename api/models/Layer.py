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


class LayerInformation(BaseModel):
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
