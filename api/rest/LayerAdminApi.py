from api.classes.LayerManager import LayerManger
from api.models.Layer import (
    AddLayerModel,
    AddNewLayerItem,
    GetAllLayers,
    GetLayerItemResponse,
    UpdateLayerModel,
)
from fastapi import APIRouter
from api.models.GlobalModels import GlobalResult
from typing import Optional

admin_layer_routes = APIRouter()


@admin_layer_routes.post(
    "/add", description="add layer", status_code=201, response_model=GlobalResult
)
async def layer_add(body: AddLayerModel):
    result = await LayerManger.Admin.add(body)
    return result


@admin_layer_routes.post(
    "/layer-item/add",
    description="add layer item",
    status_code=201,
    response_model=GlobalResult,
)
async def add_layer_item(body: AddNewLayerItem):
    result = await LayerManger.Admin.add_layer_item(body)
    return result


@admin_layer_routes.get(
    "/layers",
    description="get all layers",
    status_code=200,
    response_model=GetAllLayers,
)
async def get_all(page: Optional[int] = 1):
    result = await LayerManger.Admin.get_all(page)
    return result


@admin_layer_routes.get(
    "/layer-item/load",
    status_code=200,
    description="get layers item",
    response_model=GetLayerItemResponse,
)
async def get_layers_item(_id: str):
    result = await LayerManger.Admin.get_layers_item_of_layer(_id)
    return result


@admin_layer_routes.put("/layers/update", description="update layer", status_code=201)
async def update_layer(_id: str, body: UpdateLayerModel):
    result = await LayerManger.Admin.update(_id, body)
    return result
