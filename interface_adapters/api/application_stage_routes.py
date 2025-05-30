from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Body

from containers.container import Container
from domain.entities.application_stage import ApplicationStage
from domain.schemas.application_stage_schema import ApplicationStageSchema, ApplicationStageSchemaCreate
from use_cases.application_stage_use_cases import ApplicationStageUseCases


router = APIRouter()


@router.post("/application_stage", status_code=status.HTTP_201_CREATED, response_model=ApplicationStageSchema)
@inject
def create_application_stage(
    application_stage_data: ApplicationStageSchemaCreate = Body(...),
    application_stage_use_cases: ApplicationStageUseCases = Depends(
        Provide[Container.application_stage_use_cases]
    )
):
    application_stage = application_stage_use_cases.create_application_stage(
        ApplicationStage(
            application_stage=application_stage_data.application_stage,
        )
    )

    application_stage_json = jsonable_encoder(application_stage)

    return application_stage_json

@router.get("/application_stage", status_code=status.HTTP_200_OK, response_model=list[ApplicationStageSchema])
@inject
def get_all_application_stage(
    application_stage_use_cases: ApplicationStageUseCases = Depends(
        Provide[Container.application_stage_use_cases]
    )
):
    applications_stage = application_stage_use_cases.get_all_application_stage()
    applications_stage_json = jsonable_encoder(applications_stage)

    return applications_stage_json
