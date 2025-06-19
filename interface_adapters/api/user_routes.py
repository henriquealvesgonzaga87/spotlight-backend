import json
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, status, Body
from fastapi.encoders import jsonable_encoder
from interface_adapters.api.dependencies.dependencies import login_required
from use_cases.user_use_cases import UserUseCases
from containers.container import Container
from domain.schemas.user_schema import UserSchema, UserSchemaCreate, UserSchemaUpdate
from domain.entities.user import User


router = APIRouter(
    tags=["user"]
)


@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=UserSchema)
@inject
def create_user(user_data: UserSchemaCreate = Body(...), user_use_cases: UserUseCases = Depends(Provide[Container.user_use_cases])):
    user = user_use_cases.create_user(
        User(
            name=user_data.name, 
            email=user_data.email, 
            password=user_data.password
        ))
    user_json = jsonable_encoder(obj=user)

    return user_json


@router.get("/user/{user_id}", status_code=status.HTTP_200_OK, response_model=UserSchema)
@inject
def get_user_by_id(
    user_id: int,
    current_user_email: str = Depends(login_required),
    user_use_cases: UserUseCases = Depends(Provide[Container.user_use_cases])
):
    user = user_use_cases.get_user_by_id(user_id=user_id)
    user_json = jsonable_encoder(obj=user)

    return user_json


@router.patch("/user/{user_id}", status_code=status.HTTP_200_OK, response_model=UserSchema)
@inject
def update_user(
    user_id: int, 
    user_data: UserSchemaUpdate = Body(...),
    current_user_email: str = Depends(login_required),
    user_use_cases: UserUseCases = Depends(Provide[Container.user_use_cases])
):
    user = user_use_cases.update_user(user_id=user_id, user=User(
        name = user_data.name,
        email=user_data.email,
        password=user_data.password
    ))
    user_json = jsonable_encoder(user)

    return user_json


@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_user(
    user_id: int,
    current_user_email: str = Depends(login_required),
    user_use_cases: UserUseCases = Depends(Provide[Container.user_use_cases])
):
    response = user_use_cases.delete_user(user_id=user_id)

    return json.dumps(obj=response, indent=4)
