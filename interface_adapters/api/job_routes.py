from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Body

from containers.container import Container
from domain.entities.job import Job
from domain.schemas.job_schema import JobSchema, JobSchemaCreate, JobSchemaUpdate
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


@router.get("/job", status_code=status.HTTP_200_OK, response_model=list[JobSchema])
@inject
def get_all_jobs(job_use_cases: JobUseCases = Depends(Provide[Container.job_use_cases])):
    jobs = job_use_cases.get_all_jobs()

    jobs_json = jsonable_encoder(jobs)

    return jobs_json


@router.get("/job/{job_id}", status_code=status.HTTP_200_OK, response_model=JobSchema)
@inject
def get_job_by_id(job_id: int, job_use_cases: JobUseCases = Depends(Provide[Container.job_use_cases])):
    job = job_use_cases.get_job_by_id(job_id=job_id)

    job_json = jsonable_encoder(job)

    return job_json


@router.patch("/job/{job_id}", status_code=status.HTTP_200_OK, response_model=JobSchema)
@inject
def update_job(
    job_id: int,
    job_data: JobSchemaUpdate = Body(...),
    job_use_cases: JobUseCases = Depends(Provide[Container.job_use_cases])
):
    job_dict = job_data.model_dump(exclude_unset=True)
    job = job_use_cases.update_job(
        job_id=job_id, 
        job=job_dict
    )

    job_json = jsonable_encoder(job)

    return job_json
