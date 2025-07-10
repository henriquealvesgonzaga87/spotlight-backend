import os
import pytest

from jose import jwt
from dotenv import load_dotenv
from unittest.mock import Mock
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from domain.entities.user import User
from domain.exceptions.bad_request_error import BadRequestError
from domain.exceptions.not_found_error import NotFoundError
from domain.exceptions.unauthorized_error import UnauthorizedError
from domain.interfaces.auth_repository_interface import AuthRepositoryInterface
from domain.interfaces.redis.auth_redis_repository_interface import AuthRedisRepositoryInterface
from domain.schemas.auth_schema import LoginSchema, TokenSchema
from interface_adapters.api.dependencies.dependencies import login_required
from interface_adapters.database.redis.auth_redis_repository import RedisAuthRepository
from interface_adapters.database.redis.dependencies import RedisClient
from interface_adapters.database.sqlalchemy.auth_repository import SQLAlchemyAuthRepository
from use_cases.auth_use_cases import AuthUseCases


load_dotenv(".env.test")


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
def mock_auth_use_cases_for_routes():
    return Mock()


@pytest.fixture(scope="session")
def jwt_config():
    return {
        "secret": os.getenv("SECRET_KEY", "fake_secret"),
        "algo": os.getenv("ALGORITHM", "HS256"),
        "access_exp": timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))),
        "refresh_exp": timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))),
    }


@pytest.fixture
def access_token(jwt_config, login_data):
    now = datetime.utcnow()
    payload = {
        "sub": login_data.email,
        "iat": now,
        "exp": now + jwt_config["access_exp"]
    }
    token = jwt.encode(payload, jwt_config["secret"], algorithm=jwt_config["algo"])
    return token if isinstance(token, str) else token.decode()


@pytest.fixture
def refresh_token(jwt_config, login_data):
    now = datetime.utcnow()
    payload = {
        "sub": login_data.email,
        "iat": now,
        "exp": now + jwt_config["refresh_exp"],
        "type": "refresh"                   # opcional para diferenciar
    }
    token = jwt.encode(payload, jwt_config["secret"], algorithm=jwt_config["algo"])
    return token if isinstance(token, str) else token.decode()


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
    mock_redis_auth_repository_interface,
    refresh_token_str
):
    redis_repo = mock_redis_auth_repository_interface
    redis_repo.revoke_refresh_token.return_value = True
    redis_repo.is_refresh_token_revoked.return_value = refresh_token_str

    return redis_repo


@pytest.fixture
def mock_auth_use_cases_success(
    mock_auth_repository_interface,
    mock_redis_auth_repository_interface,
    user,
    access_token_str,
    refresh_token_str,
    token_response
):
    use_cases = AuthUseCases(
        auth_repository=mock_auth_repository_interface,
        auth_redis_repository=mock_redis_auth_repository_interface
    )
    use_cases._authenticate_user = Mock(return_value=user)
    use_cases._create_access_token = Mock(return_value=access_token_str)
    use_cases._create_refresh_token = Mock(return_value=refresh_token_str)
    use_cases.login = Mock(return_value=token_response)
    use_cases.refresh_token = Mock(return_value=token_response)

    return use_cases


@pytest.fixture
def mock_auth_use_cases_failure(
    mock_auth_repository_interface,
    mock_redis_auth_repository_interface,
):
    use_cases = AuthUseCases(
        auth_repository=mock_auth_repository_interface,
        auth_redis_repository=mock_redis_auth_repository_interface
    )
    use_cases._authenticate_user = Mock(side_effect=UnauthorizedError("error"))
    use_cases._create_access_token = Mock(side_effect=Exception("error"))
    use_cases._create_refresh_token = Mock(side_effect=Exception("error"))
    use_cases.login = Mock(side_effect=UnauthorizedError("error"))
    use_cases.refresh_token = Mock(side_effect=BadRequestError("error"))

    return use_cases


@pytest.fixture
def mock_auth_repository_failure(mock_session):
    repo = SQLAlchemyAuthRepository(session=mock_session)
    repo.get_user_by_email = Mock(side_effect=NotFoundError("error"))

    return repo


@pytest.fixture
def mock_redis_auth_repository_failure(mock_redis_client):
    redis_repo = RedisAuthRepository(redis_client=mock_redis_client)
    redis_repo.revoke_refresh_token = Mock(side_effect=Exception("error"))
    redis_repo.is_refresh_token_revoked = Mock(side_effect=Exception("error"))

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
def token_response():
    return TokenSchema(
        access_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJoZW5yaXF1ZUBtYWlsLmNvbSIsImV4cCI6MTc1MDUwMTc5OH0.VHCYCiRWHzHneN4Y-ToWfuNXc4ZPOqHxm46hyr36iuE',
        refresh_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJoZW5yaXF1ZUBtYWlsLmNvbSIsImV4cCI6MTc1MTEwNTY5OH0.C0yfkxhPvnDa9RPUwLg5FT7fYAPMhpd37bmdloa56I8',
        token_type="bearer"
    )


@pytest.fixture
def token_json_response():
    return {
            'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJoZW5yaXF1ZUBtYWlsLmNvbSIsImV4cCI6MTc1MDUwMTc5OH0.VHCYCiRWHzHneN4Y-ToWfuNXc4ZPOqHxm46hyr36iuE', 
            'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJoZW5yaXF1ZUBtYWlsLmNvbSIsImV4cCI6MTc1MTEwNTY5OH0.C0yfkxhPvnDa9RPUwLg5FT7fYAPMhpd37bmdloa56I8', 
            'token_type': 'bearer'
        }


@pytest.fixture
def access_token_str():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJoZW5yaXF1ZUBtYWlsLmNvbSIsImV4cCI6MTc1MDUwMTc5OH0.VHCYCiRWHzHneN4Y-ToWfuNXc4ZPOqHxm46hyr36iuE"


@pytest.fixture
def refresh_token_str():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJoZW5yaXF1ZUBtYWlsLmNvbSIsImV4cCI6MTc1MTEwNTY5OH0.C0yfkxhPvnDa9RPUwLg5FT7fYAPMhpd37bmdloa56I8"


@pytest.fixture
def access_token_header(access_token):
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def refresh_token_header(refresh_token):
    return {"X-Refresh-Token": f"Bearer {refresh_token}"}


@pytest.fixture
def login_data():
    return LoginSchema(
        email="test@mail.com",
        password="Admin@123456"
    )


@pytest.fixture
def create_access_token_data(login_data):
    return {"sub": login_data.email}


@pytest.fixture
def create_refresh_token_data(login_data):
    return {"sub": login_data.email}
