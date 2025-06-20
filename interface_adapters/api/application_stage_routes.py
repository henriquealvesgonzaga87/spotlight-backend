from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Body, Query

from containers.container import Container
from domain.entities.application_stage import ApplicationStage
from domain.schemas.application_stage_schema import ApplicationStageSchema, ApplicationStageSchemaCreate
from interface_adapters.api.dependencies.dependencies import login_required
from use_cases.application_stage_use_cases import ApplicationStageUseCases


router = APIRouter(
    dependencies=[Depends(login_required)],
    tags=["application_stage"]
)


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


@router.get("/application_stage/id/{application_stage_id}", status_code=status.HTTP_200_OK, response_model=ApplicationStageSchema)
@inject
def get_application_stage_by_id(
    application_stage_id: int,
    application_stage_use_cases: ApplicationStageUseCases = Depends(
        Provide[Container.application_stage_use_cases]
    )
):
    application_stage = application_stage_use_cases.get_application_stage_by_id(
        application_stage_id=application_stage_id
    )
    application_stage_json = jsonable_encoder(application_stage)

    return application_stage_json


@router.get("/application_stage/search", status_code=status.HTTP_200_OK, response_model=list[ApplicationStageSchema])
@inject
def get_application_stage_by_name(
    application_stage_data: str = Query(..., alias="application_stage"),
    application_stage_use_cases: ApplicationStageUseCases = Depends(
        Provide[Container.application_stage_use_cases]
    )
):
    application_stage = application_stage_use_cases.get_application_stage_by_name(
        application_stage=application_stage_data
    )

    application_stage_json = jsonable_encoder(application_stage)

    return application_stage_json


@router.patch("/application_stage/{application_stage_id}", status_code=status.HTTP_200_OK, response_model=ApplicationStageSchema)
@inject
def update_application_state(
    application_stage_id: int,
    application_stage_data: ApplicationStageSchemaCreate = Body(...),
    application_stage_use_cases: ApplicationStageUseCases = Depends(
        Provide[Container.application_stage_use_cases]
    )
):
    application_stage = application_stage_use_cases.update_application_stage(
        application_stage_id=application_stage_id,
        application_stage=ApplicationStage(
            application_stage=application_stage_data.application_stage
        )
    )

    application_stage_json = jsonable_encoder(application_stage)

    return application_stage_json


@router.delete("/application_stage/{application_stage_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_application_stage(
    application_stage_id: int,
    application_stage_use_cases: ApplicationStageUseCases = Depends(
        Provide[Container.application_stage_use_cases]
    )
):
    application_stage = application_stage_use_cases.delete_application_stage(
        application_stage_id=application_stage_id
    )

    return {"message": f"{application_stage} deleted successfully"}
