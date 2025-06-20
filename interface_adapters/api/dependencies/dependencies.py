import os

from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, ExpiredSignatureError, JWTError
from dependency_injector.wiring import inject, Provide

from containers.container import Container
from domain.exceptions.unauthorized_error import UnauthorizedError
from use_cases.auth_use_cases import AuthUseCases


load_dotenv()

bearer_schema = HTTPBearer(auto_error=False)


@inject
def login_required(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_schema)],
    auth_use_cases: AuthUseCases = Depends(Provide[Container.auth_use_cases])
):
    if credentials is None:
        raise UnauthorizedError("Missing Authorization header: WWW-Authenticate: Bearer")
    
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token=token,
            key=os.getenv("SECRET_KEY"),
            algorithms=os.getenv("ALGORITHM"),
        )

        email: str | None = payload.get("sub")

        if email is None:
            raise JWTError()
        
        user = auth_use_cases.get_user_by_email(email=email)
        
        return user
        
    except ExpiredSignatureError:
        raise UnauthorizedError("Access-token expired. WWW-Authenticate: Bearer")
    
    except JWTError as e:
        raise UnauthorizedError(f"Invalid Token. WWW-Authenticate: Bearer. !!!{e}")
