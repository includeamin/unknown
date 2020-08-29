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
    UpdateLayerModel,
    GetListOfCodeFileNames,
)
from api.db.mongo import layer_collection
from api.models.GlobalModels import GlobalResult
from fastapi import HTTPException
from datetime import timedelta, datetime, date
from typing import List, Optional, Dict
from api.utils.Tools import Tools
from src.models.Location import Coordinate
from api.classes.Storage import Storage
from api.models.Map import LayerOptionModel


class LayerManger:
    class Admin:
        @staticmethod
        async def add(data: AddLayerModel):
            await LayerManger.Shared.is_code_exist(data.code)
            layer = layer_collection.insert_one(Layer(**data.dict()).dict())
            return GlobalResult(message=str(layer.inserted_id))

        @staticmethod
        async def add_layer_item(data: AddNewLayerItem):
            layer = await LayerManger.Shared.exist_id(data)
            item_layer_id = ObjectId()
            file_name = LayerManger.Shared.get_file_name(
                item_layer_id,
                data.information.range.start,
                data.information.range.end,
                data.raw_file_name,
            )
            await LayerManger.Shared.move_layer_from_raws(
                data.raw_file_name, file_name, layer_id=data.layer_id
            )
            await LayerManger.Shared.conflict_finder(layer.code, data.information)
            item = LayerItem(**data.dict())
            item.file_name = file_name
            item.id = item_layer_id
            result = layer_collection.update_one(
                {"code": layer.code}, {"$addToSet": {"layers": item.dict()}},
            )
            await Tools.update_result_checker(result)
            return GlobalResult(message="done")

        @staticmethod
        async def delete_layer_item(item_id: str, _id: str):
            result = await LayerManger.Shared.is_exist_layer_item_with_id(_id, item_id)
            file_name = result["file_name"]
            result = layer_collection.update_one(
                {"_id": ObjectId(_id)},
                {"$pull": {"layers": {"id": ObjectId(item_id)}}},
            )
            await Tools.update_result_checker(result)
            await Storage(layer_id=_id).delete(file_name)
            return GlobalResult(message="done")

        @staticmethod
        async def update(_id: str, body: UpdateLayerModel):
            update_value = {}
            if body.code:
                update_value.update({"code": body.code})
                await LayerManger.Shared.is_code_exist(body.code, should_exist=False)
            if body.location:
                update_value.update({"location": body.location.dict()})
            if body.description:
                update_value.update({"description": body.description})
            if body.name:
                update_value.update({"code": body.name})
            if not update_value:
                raise HTTPException(detail="nothings for update", status_code=400)
            result = layer_collection.update_one(
                {"_id": ObjectId(_id)}, {"$set": update_value}
            )
            await Tools.update_result_checker(result)
            return GlobalResult(message="done")

        @staticmethod
        async def remove(_id: str):
            layer_collection.delete_one({"_id": ObjectId(_id)})
            return GlobalResult(message="done")

        @staticmethod
        async def get(_id):
            result = layer_collection.find_one({"_id": ObjectId(_id)})
            for item in result["layers"]:
                item["id"] = str(item["id"])
            return Tools.mongodb_id_converter(result)

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
        async def exist_id(data):
            result = layer_collection.find_one(
                {"_id": ObjectId(data.layer_id)}, {"layers": 0}
            )
            if not result:
                raise HTTPException(
                    detail=f"layer with {data.layer_id} not exist", status_code=404
                )
            return LayerInDB(**Tools.mongodb_id_converter(result))

        @staticmethod
        async def is_exist_layer_item_with_id(_id, item_id):
            pipe_line = [
                {"$match": {"_id": ObjectId(_id)}},
                {
                    "$project": {
                        "layers": {
                            "$filter": {
                                "input": "$layers",
                                "as": "layer",
                                "cond": {"$eq": ["$$layer.id", ObjectId(item_id)]},
                            }
                        }
                    }
                },
            ]
            result: Optional[dict] = None
            for item in layer_collection.aggregate(pipeline=pipe_line):
                if item["layers"]:
                    result = item["layers"][0]
            if not result:
                raise HTTPException(detail="item layers not found", status_code=404)
            return result

        @staticmethod
        async def get_layers_file_names(
            data: List[LayerOptionModel],
        ) -> List[GetListOfCodeFileNames]:
            """
            :param data:
            :return: list of file_name
            """
            layer_ids: Optional[List[ObjectId]] = []
            layer_item_ids: Optional[List[ObjectId]] = []
            for requested_layer in data:
                layer_ids.append(ObjectId(requested_layer.layer_id))
                layer_item_ids.append(ObjectId(requested_layer.layer_item_id))

            pipe_line = [
                {"$match": {"_id": {"$in": layer_ids}}},
                {
                    "$project": {
                        "layers": {
                            "$filter": {
                                "input": "$layers",
                                "as": "layer",
                                "cond": {"$in": ["$$layer.id", layer_item_ids]},
                            }
                        },
                        "code": "$code",
                    }
                },
            ]
            list_of_file_names: List[GetListOfCodeFileNames] = []
            for item in layer_collection.aggregate(pipeline=pipe_line):
                [
                    list_of_file_names.append(
                        GetListOfCodeFileNames(
                            file_name=f"{str(item['_id'])}/{d['file_name']}",
                            code=item["code"],
                        )
                    )
                    for d in item["layers"]
                ]

            return list_of_file_names

        @staticmethod
        def get_file_name(
            item_id: ObjectId, start: datetime, end: datetime, raw_file_name: str
        ):
            return (
                f"{str(item_id)}-{start.date()}-{end.date()}."
                f"{raw_file_name.split('.')[-1]}"
            )

        @staticmethod
        async def move_layer_from_raws(
            raw_file_name: str, new_file_name: str, layer_id: str
        ):
            await Storage(
                raw_file=raw_file_name, new_name=new_file_name, layer_id=layer_id
            ).move()

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
                resp.append(ValidLayers(**Tools.mongodb_id_converter(item)))
            return ValidLayersNearLocation(results=resp, page=page)

        @staticmethod
        async def is_code_exist(code: str, should_exist: bool = False):
            result = layer_collection.find_one({"code": code}, {})
            if result and not should_exist:
                raise HTTPException(
                    detail=f"layer with {code} code already exist", status_code=400
                )
            if not result and should_exist:
                raise HTTPException(
                    detail=f"layer with{code} code not exist", status_code=404
                )
            if should_exist:
                return str(result["_id"])

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
                    timedelta(days=0),
                    min(event["end"], end) - max(event["start"], start),
                )
                if overlap > timedelta(days=0):
                    overlaps.append(event)
            if overlaps:
                raise HTTPException(detail=f"{overlaps}", status_code=403)
