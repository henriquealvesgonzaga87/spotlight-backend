import os
import pytest

from dotenv import load_dotenv
from datetime import datetime, timedelta
from jose import jwt

from domain.schemas.auth_schema import LoginSchema


load_dotenv(".env.test")


@pytest.fixture
def login_data():
    return LoginSchema(
        email="admin@mail.com",
        password="Admin@123456"
    )


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
def access_token_header(access_token):
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def refresh_token_header(refresh_token):
    return {"X-Refresh-Token": f"Bearer {refresh_token}"}


@pytest.fixture
def headers(access_token_header, refresh_token_header):
    return {**access_token_header, **refresh_token_header}
