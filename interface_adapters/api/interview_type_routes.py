from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Body

from containers.container import Container
from domain.entities.interview_type import InterviewType
from domain.schemas.interview_type_schema import InterviewTypeSchema, InterviewTypeSchemaCreate
from interface_adapters.api.dependencies.dependencies import login_required
from use_cases.interview_type_use_cases import InterviewTypeUseCases


router = APIRouter(
    tags=["interview_type"]
)


@router.post("/interview_type", status_code=status.HTTP_201_CREATED, response_model=InterviewTypeSchema)
@inject
def create_interview_type(
    interview_type_data: InterviewTypeSchemaCreate = Body(...),
    interview_type_use_cases: InterviewTypeUseCases = Depends(Provide[Container.interview_type_use_cases]),
    current_user: str = Depends(login_required),
):
    interview_type_dict = interview_type_data.model_dump()
    interview_type = interview_type_use_cases.create_interview_type(
        interview_type=InterviewType(
            **interview_type_dict
        )
    )

    interview_type_json = jsonable_encoder(interview_type)

    return interview_type_json


@router.get("/interview_type", status_code=status.HTTP_200_OK, response_model=list[InterviewTypeSchema])
@inject
def get_all_interview_type(
    interview_type_use_cases: InterviewTypeUseCases = Depends(Provide[Container.interview_type_use_cases]),
    current_user: str = Depends(login_required),
):
    interview_type = interview_type_use_cases.get_all_interview_type(user_id=current_user.id)

    interview_type_json = jsonable_encoder(interview_type)

    return interview_type_json


@router.get("/interview_type/{interview_type_id}", status_code=status.HTTP_200_OK, response_model=InterviewTypeSchema)
@inject
def get_interview_type_by_id(
    interview_type_id: int,
    interview_type_use_cases: InterviewTypeUseCases = Depends(Provide[Container.interview_type_use_cases]),
    current_user: str = Depends(login_required),
):
    interview_type = interview_type_use_cases.get_interview_type_by_id(
        interview_type_id=interview_type_id,
        user_id=current_user.id
    )

    interview_type_json = jsonable_encoder(interview_type)

    return interview_type_json


@router.patch("/interview_type/{interview_type_id}", status_code=status.HTTP_200_OK, response_model=InterviewTypeSchema)
@inject
def update_interview_type(
    interview_type_id: int,
    interview_type_data: InterviewTypeSchemaCreate = Body(...),
    interview_type_use_cases: InterviewTypeUseCases = Depends(Provide[Container.interview_type_use_cases]),
    current_user: str = Depends(login_required),
):
    interview_type_dict = interview_type_data.model_dump()
    interview_type = interview_type_use_cases.update_interview_type(
        interview_type_id=interview_type_id,
        interview_type=InterviewType(
            **interview_type_dict
        )
    )

    interview_type_json = jsonable_encoder(interview_type)

    return interview_type_json


@router.delete("/interview_type/{interview_type_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_interview_type(
    interview_type_id: int,
    interview_type_use_cases: InterviewTypeUseCases = Depends(Provide[Container.interview_type_use_cases]),
    current_user: str = Depends(login_required),
):
    interview_type_use_cases.delete_interview_type(interview_type_id=interview_type_id)

    return {"message": "Deleted successfully"}
