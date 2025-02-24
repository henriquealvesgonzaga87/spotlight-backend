from fastapi import FastAPI, APIRouter
from pydantic_settings import BaseSettings
from interface_adapters.api import user_routes, root_routes
from containers.user_container import UserContainer
from starlette.middleware.cors import CORSMiddleware


class App:
    def __init__(self, settings: BaseSettings, router: APIRouter) -> None:
        self.user_container: UserContainer = UserContainer()
        self.user_container.init_resources()
        self.user_container.wire(modules=[
            "interface_adapters.api.root_routes",
            "interface_adapters.api.user_routes"
        ])

        self.app = FastAPI(title=settings.PROJECT_NAME, root_path=settings.ROOT_PATH)
        self.app.include_router(router=router, prefix=settings.PREFIX)
        self.app.include_router(root_routes.router)
        self.app.include_router(user_routes.router)

        origins = ['*']

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )

    @classmethod
    def get_app(cls, settings: BaseSettings, router: APIRouter) -> FastAPI:
        app_instance = cls(settings=settings, router=router)
        return app_instance.app
