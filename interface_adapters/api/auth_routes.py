import os

from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Header, status, Depends, Body

from containers.container import Container
from domain.schemas.auth_schema import LoginSchema, TokenSchema
from interface_adapters.api.dependencies.dependencies import login_required
from use_cases.auth_use_cases import AuthUseCases


load_dotenv()


router = APIRouter(
    tags=["auth"]
)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenSchema)
@inject
def login(
    login_data: LoginSchema = Body(...),
    auth_use_cases: AuthUseCases = Depends(Provide[Container.auth_use_cases])
):
    login_data_dict = login_data.model_dump()

    tokens = auth_use_cases.login(
        login_data=LoginSchema(**login_data_dict)
    )

    tokens_json = jsonable_encoder(obj=tokens)
    
    return tokens_json


@router.post("/refresh-token", status_code=status.HTTP_200_OK, response_model=TokenSchema)
@inject
def refresh_token(
    refresh_token: str = Header(..., alias="X-Refresh-Token"),
    current_user_email: str = Depends(login_required),
    auth_use_cases: AuthUseCases = Depends(Provide[Container.auth_use_cases])
):
    tokens = auth_use_cases.refresh_token(refresh_token=refresh_token)
    
    tokens_json = jsonable_encoder(obj=tokens)
    
    return tokens_json


@router.post("/logout", status_code=status.HTTP_200_OK)
@inject
def logout(
    refresh_token: str = Header(..., alias="X-Refresh-Token"),
    current_user_email: str = Depends(login_required),
    auth_use_cases: AuthUseCases = Depends(Provide[Container.auth_use_cases])
):
    auth_use_cases.revoke_refresh_token(
        refresh_token=refresh_token,
        expires_in=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
    )

    return {"message": "Logout successful"}
