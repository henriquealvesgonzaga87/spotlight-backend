from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Body

from containers.container import Container
from domain.entities.interview import Interview
from domain.schemas.interview_schema import InterviewSchema, InterviewSchemaCreate, InterviewSchemaUpdate
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


@router.get("/interview", status_code=status.HTTP_200_OK, response_model=list[InterviewSchema])
@inject
def get_all_interview(
    interview_use_cases: InterviewUseCases = Depends(Provide[Container.interview_use_cases])
):
    interviews = interview_use_cases.get_all_interview()

    interviews_json = jsonable_encoder(interviews)

    return interviews_json


@router.get("/interview/{interview_id}", status_code=status.HTTP_200_OK, response_model=InterviewSchema)
@inject
def get_interview_by_id(
    interview_id: int,
    interview_use_cases: InterviewUseCases = Depends(Provide[Container.interview_use_cases])
):
    interview = interview_use_cases.get_interview_by_id(
        interview_id=interview_id
    )

    interview_json = jsonable_encoder(interview)

    return interview_json


@router.patch("/interview/{interview_id}", status_code=status.HTTP_200_OK, response_model=InterviewSchema)
@inject
def update_interview(
    interview_id: int,
    interview_data: InterviewSchemaUpdate = Body(...),
    interview_use_cases: InterviewUseCases = Depends(Provide[Container.interview_use_cases])
):
    interview_dict = interview_data.model_dump(exclude_unset=True)
    interview = interview_use_cases.update_interview(
        interview_id=interview_id,
        interview=interview_dict
    )

    interview_json = jsonable_encoder(interview)

    return interview_json
