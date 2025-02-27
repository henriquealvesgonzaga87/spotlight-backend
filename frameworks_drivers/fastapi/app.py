from fastapi import FastAPI, APIRouter, Request
from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError
from pydantic_settings import BaseSettings
from domain.exceptions.error_handler import ErrorHandler
from domain.exceptions.response_validation_error import ResponseValidationError
from interface_adapters.api import user_routes, root_routes
from containers.container import Container
from starlette.middleware.cors import CORSMiddleware


class App:
    def __init__(self, settings: BaseSettings, router: APIRouter) -> None:
        self.user_container: Container = Container()
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

        @self.app.exception_handler(ResponseValidationError)
        async def response_validation_error(request: Request, exc: ResponseValidationError):
            return ErrorHandler.response_validation_error_handler(request=request, exc=exc)


        @self.app.exception_handler(SQLAlchemyIntegrityError)
        async def integrity_error(request: Request, exc: SQLAlchemyIntegrityError):
            return ErrorHandler.integrity_error_handler(request=request, exc=exc)

    @classmethod
    def get_app(cls, settings: BaseSettings, router: APIRouter) -> FastAPI:
        app_instance = cls(settings=settings, router=router)
        return app_instance.app
