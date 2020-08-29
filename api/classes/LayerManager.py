from api.models.Layer import Layer, LayerInDB, AddLayerModel, LayerInformation
from api.db.mongo import layer_collection
from api.models.GlobalModels import GlobalResult
from fastapi import HTTPException
from datetime import timedelta, datetime, date
from typing import List


class LayerManger:
    class Admin:
        @staticmethod
        async def add(data: AddLayerModel):
            await LayerManger.Shared.is_code_exist(data)
            layer = layer_collection.insert_one(Layer(**data.dict()).dict())
            return GlobalResult(message=str(layer.inserted_id))

        @staticmethod
        async def update():
            pass

        @staticmethod
        async def remove():
            pass

        @staticmethod
        async def get():
            pass

    class Shared:
        @staticmethod
        async def is_code_exist(data):
            result = layer_collection.find_one({"code": data.code}, {})
            if result:
                raise HTTPException(detail=f'layer with {data.code} code already exist', status_code=400)

        @staticmethod
        async def conflict_finder(code: str, data: LayerInformation):
            result = layer_collection.find({"code": code}, {"information.range"})
            information = [item["information"]["range"] for item in result]
            LayerManger.Shared.overlap_checking(
                information, data.range.start, data.range.end
            )

        @staticmethod
        def overlap_checking(events, start: datetime, end: datetime):
            start: date = start.date()
            end: date = end.date()
            overlaps: List[datetime] = []
            for event in events:
                event["start"] = event["start"].date()
                event["end"] = event["end"].date()
                overlap = max(
                    timedelta.min, min(event["end"], end) - max(event["start"], start)
                )
                if overlap > timedelta.min:
                    overlaps.append(event)
            if overlaps:
                raise HTTPException(
                    detail=f"one or more overlap {overlaps}", status_code=400
                )
