import importlib.util
import json
import os

import requests
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware


from api.service.pretty_response import PrettyJSONResponse
from api.service.instance_manager import close_running_instance

with open("config.json") as f:
    config = json.load(f)

close_running_instance(config)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get('/')
async def index():
    response = RedirectResponse(url='/ping')
    return response


@app.get('/ping/')
async def ping():
    response = {"response": "I am trained on {} Machine Learning Models using {} datapoints."}
    return PrettyJSONResponse(content=response)


@app.get('/urls/')
async def urls():
    response = {"response": app.openapi().get("paths")}
    return PrettyJSONResponse(response)


with open("api/route/routes.json") as f:
    routes = json.load(f)

for route in routes:
    importlib.util.spec_from_file_location(route, f"api/route/{route}.py")
    module = importlib.import_module(f"api.route.{route}")
    module.setup(app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host=config.get("host"), port=config.get("port"))
