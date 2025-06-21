import pytest

from unittest.mock import Mock
from sqlalchemy.orm import Session

from domain.entities.user import User
from domain.exceptions.not_found_error import NotFoundError
from domain.interfaces.auth_repository_interface import AuthRepositoryInterface
from domain.interfaces.redis.auth_redis_repository_interface import AuthRedisRepositoryInterface
from interface_adapters.database.redis.auth_redis_repository import RedisAuthRepository
from interface_adapters.database.redis.dependencies import RedisClient
from interface_adapters.database.sqlalchemy.auth_repository import SQLAlchemyAuthRepository
from use_cases.auth_use_cases import AuthUseCases


@pytest.fixture
def mock_session():
    return Mock(spec=Session)


@pytest.fixture
def mock_redis_client():
    return Mock(spec=RedisClient)


@pytest.fixture
def mock_auth_repository_interface():
    return Mock(spec=AuthRepositoryInterface)


@pytest.fixture
def mock_redis_auth_repository_interface():
    return Mock(spec=AuthRedisRepositoryInterface)


@pytest.fixture
def mock_auth_use_cases():
    return Mock(spec=AuthUseCases)


@pytest.fixture
def mock_auth_repository_success(
    mock_auth_repository_interface,
    user
):
    repo = mock_auth_repository_interface
    repo.get_user_by_email.return_value = user

    return repo


@pytest.fixture
def mock_redis_auth_repository_success(
    mock_redis_auth_repository_interface
):
    redis_repo = mock_redis_auth_repository_interface
    redis_repo.revoke_refresh_token.return_value = True

    return redis_repo


@pytest.fixture
def mock_auth_repository_failure(mock_session):
    repo = SQLAlchemyAuthRepository(session=mock_session)
    repo.get_user_by_email = Mock(side_effect=NotFoundError("error"))

    return repo


@pytest.fixture
def mock_redis_auth_repository_failure(mock_redis_client):
    redis_repo = RedisAuthRepository(redis_client=mock_redis_client)
    redis_repo.revoke_refresh_token = Mock(side_effect=Exception("error"))

    return redis_repo


@pytest.fixture
def user():
    return User(
        id= 1,
        name= "test",
        email= "test@mail.com",
        password= "$2b$12$AsaPjprPnvV49UcgRwc1HOdljdWpqrzjURduQp3imZuWd5UG1wMnO",
        created_at= "2025-06-03T16:17:08.057764",
        updated_at= None
    )


@pytest.fixture
def token_json_reposnse():
    return {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJoZW5yaXF1ZUBtYWlsLmNvbSIsImV4cCI6MTc1MDUwMTc5OH0.VHCYCiRWHzHneN4Y-ToWfuNXc4ZPOqHxm46hyr36iuE",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJoZW5yaXF1ZUBtYWlsLmNvbSIsImV4cCI6MTc1MTEwNTY5OH0.C0yfkxhPvnDa9RPUwLg5FT7fYAPMhpd37bmdloa56I8",
        "token_type": "bearer"
    }


@pytest.fixture
def refresh_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJoZW5yaXF1ZUBtYWlsLmNvbSIsImV4cCI6MTc1MTEwNTY5OH0.C0yfkxhPvnDa9RPUwLg5FT7fYAPMhpd37bmdloa56I8"
