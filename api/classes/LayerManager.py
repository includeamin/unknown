from bson import ObjectId

from api.models.Layer import (
    Layer,
    LayerInDB,
    AddLayerModel,
    LayerInformation,
    AddNewLayerItem,
    LayerItem,
    ValidLayers,
    ValidLayersNearLocation,
    GetAllLayers,
    GetLayerItemResponse,
)
from api.db.mongo import layer_collection
from api.models.GlobalModels import GlobalResult
from fastapi import HTTPException
from datetime import timedelta, datetime, date
from typing import List
from api.utils.Tools import Tools
from src.models.Location import Coordinate


class LayerManger:
    class Admin:
        @staticmethod
        async def add(data: AddLayerModel):
            await LayerManger.Shared.is_code_exist(data.code)
            layer = layer_collection.insert_one(Layer(**data.dict()).dict())
            return GlobalResult(message=str(layer.inserted_id))

        @staticmethod
        async def add_layer_item(data: AddNewLayerItem):
            await LayerManger.Shared.is_code_exist(code=data.code, should_exist=True)
            file_name = (
                f"{data.code}-{data.information.range.start.date()}-{data.information.range.end.date()}."
                f"{data.raw_file_name.split('.')[-1]}"
            )
            await LayerManger.Shared.move_layer_from_raws(data.raw_file_name, file_name)
            await LayerManger.Shared.conflict_finder(data.code, data.information)
            item = LayerItem(**data.dict())
            item.file_name = file_name
            result = layer_collection.update_one(
                {"code": data.code}, {"$addToSet": {"layers": item.dict()}},
            )
            await Tools.update_result_checker(result)
            return GlobalResult(message="done")

        @staticmethod
        async def delete_layer_item(information: LayerInformation, _id: str):
            result = layer_collection.update_one({"_id": ObjectId(_id)}, {
                "$pull": {"layers": {"$elemMatch": {"information": information.dict()}}}})
            await Tools.update_result_checker(result)
            return GlobalResult(message='done')

        @staticmethod
        async def update():
            pass

        @staticmethod
        async def remove(_id: str):
            layer_collection.delete_one({"_id": ObjectId(_id)})
            return GlobalResult(message='done')

        @staticmethod
        async def get():
            pass

        @staticmethod
        async def get_layers_item_of_layer(_id: str) -> GetLayerItemResponse:
            result = layer_collection.find_one({"_id": ObjectId(_id)})
            result = Layer(**result)
            return GetLayerItemResponse(layers=result.layers)

        @staticmethod
        async def get_all(page: int):
            paging = Tools.pagination(page)
            result = (
                layer_collection.find({}, {"layers": 0})
                    .limit(paging.limit)
                    .skip(paging.skip)
            )
            result = [LayerInDB(**Tools.mongodb_id_converter(item)) for item in result]
            return GetAllLayers(result=result, page=page)

    class Shared:
        @staticmethod
        async def move_layer_from_raws(raw_file_name: str, new_file_name: str):
            pass

        @staticmethod
        async def find_available_layers_near_coordinate(
                coordinate: Coordinate, page: int = 1
        ):
            paging = Tools.pagination(page)
            result = (
                layer_collection.find(
                    {
                        "location": {
                            "$near": {
                                "$geometry": {
                                    "type": "Point",
                                    "coordinates": [
                                        coordinate.longitude,
                                        coordinate.latitude,
                                    ],
                                }
                            }
                        }
                    }
                )
                    .limit(paging.limit)
                    .skip(paging.skip)
            )
            resp = []
            for item in result:
                resp.append(ValidLayers(**item))
            return ValidLayersNearLocation(results=resp, page=page)

        @staticmethod
        async def is_code_exist(code: str, should_exist: bool = False):
            result = layer_collection.find_one({"code": code}, {})
            if result and not should_exist:
                raise HTTPException(
                    detail=f"layer with {code} code already exist", status_code=400
                )
            if not result and should_exist:
                return HTTPException(
                    detail=f"layer with{code} code not exist", status_code=404
                )

        @staticmethod
        async def conflict_finder(code: str, data: LayerInformation):
            result = layer_collection.find_one({"code": code}, {"layers"})
            information = [item["information"]["range"] for item in result["layers"]]
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
