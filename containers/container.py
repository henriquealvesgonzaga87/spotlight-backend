from dependency_injector import containers, providers
from interface_adapters.database.sqlalchemy.dependencies import get_db
from interface_adapters.database.sqlalchemy.user_repository import SQLAlchemyUserRepository
from use_cases.user_use_cases import UserUseCases
from settings import get_settings


settings = get_settings()

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        "interface_adapters.api.user_routes",    
    ])

    data_base_session = providers.Resource(get_db)

    user_repository = providers.Factory(SQLAlchemyUserRepository, session=data_base_session)
    user_use_cases = providers.Factory(UserUseCases, user_repository=user_repository)
