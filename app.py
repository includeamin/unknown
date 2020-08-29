from fastapi import FastAPI
from uvicorn import run
from api.rest.MapApi import user_map_routes
from api.rest.LayerAdminApi import admin_layer_routes
from fastapi.responses import UJSONResponse

app = FastAPI()
app.include_router(user_map_routes, tags=["MAP"], default_response_class=UJSONResponse)
app.include_router(
    admin_layer_routes, tags=["AdminLayer"], default_response_class=UJSONResponse
)

if __name__ == "__main__":
    run(app, port=3000)
