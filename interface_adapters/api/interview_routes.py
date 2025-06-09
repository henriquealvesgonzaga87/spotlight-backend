from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Body

from containers.container import Container
from domain.entities.interview import Interview
from domain.schemas.interview_schema import InterviewSchema, InterviewSchemaCreate
from use_cases.interview_use_cases import InterviewUseCases


router = APIRouter()


@router.post("/interview", status_code=status.HTTP_201_CREATED, response_model=InterviewSchema)
@inject
def create_interview(
    interview_data: InterviewSchemaCreate = Body(...),
    interview_use_cases: InterviewUseCases = Depends(Provide[Container.interview_use_cases])
):
    interview_dict = interview_data.model_dump()
    interview = interview_use_cases.create_interview(
        interview=Interview(
            **interview_dict
        )
    )

    interview_json = jsonable_encoder(interview)

    return interview_json
