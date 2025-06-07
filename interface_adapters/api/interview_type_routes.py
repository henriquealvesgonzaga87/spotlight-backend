from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Body

from containers.container import Container
from domain.entities.interview_type import InterviewType
from domain.schemas.interview_type_schema import InterviewTypeSchema, InterviewTypeSchemaCreate
from use_cases.interview_type_use_cases import InterviewTypeUseCases


router = APIRouter()


@router.post("/interview_type", status_code=status.HTTP_201_CREATED, response_model=InterviewTypeSchema)
@inject
def create_interview_type(
    interview_type_data: InterviewTypeSchemaCreate = Body(...),
    interview_type_use_cases: InterviewTypeUseCases = Depends(Provide[Container.interview_type_use_cases])
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
    interview_type_use_cases: InterviewTypeUseCases = Depends(Provide[Container.interview_type_use_cases])
):
    interview_type = interview_type_use_cases.get_all_interview_type()

    interview_type_json = jsonable_encoder(interview_type)

    return interview_type_json
