from api.settings import api_settings
from fastapi import HTTPException
import uuid
from random import randint
from bson.objectid import ObjectId
from pydantic import BaseModel


class PaginationModel(BaseModel):
    limit: int
    skip: int


class Tools:
    PAGE_SIZE = api_settings.MAX_PAGE

    @staticmethod
    def pagination(page=1) -> PaginationModel:
        x = page - 1
        skip = Tools.PAGE_SIZE * x
        return PaginationModel(limit=Tools.PAGE_SIZE, skip=skip)

    @staticmethod
    def mongodb_id_converter(data: dict) -> dict:
        data["id"] = str(data["_id"])
        data.pop("_id")
        return data

    @staticmethod
    async def combine_two_list(list_one: list, list_two: list) -> list:
        return list(set(list_one + list_two))

    @staticmethod
    async def update_result_checker(result, message: str = "nothing has been updated"):
        if result.modified_count == 0:
            raise HTTPException(detail=message, status_code=400)

    @staticmethod
    async def secret_key_generator():
        return str(uuid.uuid4())

    @staticmethod
    async def code_generator():
        return randint(1000, 9999)

    @staticmethod
    def is_valid_object_id(_id: str):
        if not ObjectId.is_valid(_id):
            raise HTTPException(detail="invalid id", status_code=400)
