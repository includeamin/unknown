from fastapi import FastAPI
from uvicorn import run
from api.rest.MapApi import user_map_routes

app = FastAPI()
app.include_router(user_map_routes)

if __name__ == "__main__":
    run(app, port=3000)
