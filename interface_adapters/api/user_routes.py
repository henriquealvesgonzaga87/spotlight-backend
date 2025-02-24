from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, status
from use_cases.user_use_cases import UserUseCases
from containers.user_container import UserContainer
from domain.schemas.user_schema import UserSchema, UserSchemaCreate
from domain.entities.user import User


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"message": "Hello World"}


@inject
@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=UserSchema)
def create_user(user_data: UserSchemaCreate, user_use_cases: UserUseCases = Depends(Provide[UserContainer.user_use_cases])):
    user = user_use_cases.create_user(User(name=user_data.name, email=user_data.email))
    return user
    
