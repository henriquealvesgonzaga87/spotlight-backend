from fastapi import APIRouter, status, Depends
from dependency_injector.wiring import inject, Provide

from containers.container import Container
from use_cases.location_use_cases import LocationUseCases


router = APIRouter()


@router.post("/location/country", status_code=status.HTTP_201_CREATED)
@inject
def create_country(location_use_cases: LocationUseCases = Depends(Provide[Container.location_use_cases])):
    location_use_cases.create_country()

    return "seeded successfully"
