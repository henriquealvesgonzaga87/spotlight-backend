import os

from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from interface_adapters.database.sqlalchemy.user_repository import SQLAlchemyUserRepository
from use_cases.user_use_cases import UserUseCases


class UserContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["interface_adapters.api.user_routes"])

    engine = providers.Singleton(create_engine, os.getenv('DATABASE_URL'), connect_args={"check_same_thread": False})
    session_factory = providers.Singleton(sessionmaker, bind=engine)

    user_repository = providers.Factory(SQLAlchemyUserRepository, session=session_factory)
    user_use_cases = providers.Factory(UserUseCases, user_repository=user_repository)
