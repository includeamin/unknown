from fastapi import APIRouter
from api.classes.Map import Map
from api.classes.LayerManager import LayerManger
from api.models.Layer import ValidLayersNearLocation

from api.models.Map import WebMapRequestModel
from src.models.Location import Coordinate

user_map_routes = APIRouter()


@user_map_routes.post("/map")
async def map_process(body: WebMapRequestModel):
    results = await Map.request(request_model=body)
    return results


@user_map_routes.get("/map/available-layers", description='get available layers', status_code=200,
                     response_model=ValidLayersNearLocation)
async def get_available_layers(longitude: float, latitude: float):
    result = await LayerManger.Shared.find_available_layers_near_coordinate(
        Coordinate(longitude=longitude, latitude=latitude))
    return result
