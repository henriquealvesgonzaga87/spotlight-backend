from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Body

from containers.container import Container
from domain.schemas.auth_schema import LoginSchema, TokenSchema
from use_cases.auth_use_cases import AuthUseCases


router = APIRouter()


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
