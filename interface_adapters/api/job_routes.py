from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Body

from containers.container import Container
from domain.entities.job import Job
from domain.schemas.job_schema import JobSchema, JobSchemaCreate
from use_cases.job_use_cases import JobUseCases


router = APIRouter()


@router.post("/job", status_code=status.HTTP_201_CREATED, response_model=JobSchema)
@inject
def create_job(job_data: JobSchemaCreate = Body(...), job_use_cases: JobUseCases = Depends(Provide[Container.job_use_cases])):
    job_dict = job_data.model_dump()
    job = job_use_cases.create_job(
        job=Job(**job_dict)
    )

    job_json = jsonable_encoder(job)

    return job_json
