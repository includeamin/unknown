from fastapi import APIRouter
from api.classes.Map import Map

from api.models.Map import WebMapRequestModel

user_map_routes = APIRouter()


@user_map_routes.post("/map")
async def map_process(body: WebMapRequestModel):
    results = await Map.request(request_model=body)
    return results
