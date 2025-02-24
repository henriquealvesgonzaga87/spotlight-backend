from fastapi import FastAPI
from interface_adapters.api import user_routes
from containers.user_container import UserContainer

app = FastAPI()

container = UserContainer()
container.init_resources()
container.wire(modules=["interface_adapters.api.user_routes"])

app.include_router(user_routes.router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}
