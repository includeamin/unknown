from api.classes.LayerManager import LayerManger
from api.models.Layer import AddLayerModel
from fastapi import APIRouter
from api.models.GlobalModels import GlobalResult

admin_layer_routes = APIRouter()


@admin_layer_routes.post(
    "/add", description="add layer", status_code=201, response_model=GlobalResult
)
async def layer_add(body: AddLayerModel):
    result = await LayerManger.Admin.add(body)
    return result


# @admin_layer_routes.get("/test")
# async def test():
#     await LayerManger.Shared.find_available_layers_near_coordinate(None)
