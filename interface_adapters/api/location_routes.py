from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide

from containers.container import Container
from domain.entities.location import City
from domain.schemas.location_schema import CityCreateSchema, CitySchema
from use_cases.location_use_cases import LocationUseCases


router = APIRouter()


@router.post("/location/country", status_code=status.HTTP_201_CREATED)
@inject
def create_country(location_use_cases: LocationUseCases = Depends(Provide[Container.location_use_cases])):
    location_use_cases.create_country()

    return "seeded successfully"


@router.post("/location/city", status_code=status.HTTP_201_CREATED, response_model=CitySchema)
@inject
def create_city(city_data: CityCreateSchema, location_use_case: LocationUseCases = Depends(Provide[Container.location_use_cases])):
    city = location_use_case.create_city(city=City(
        name=city_data.name,
        country_id=city_data.country_id
    ))

    city_json = jsonable_encoder(obj=city)

    return city_json


@router.post("/location", status_code=status.HTTP_201_CREATED)
@inject
def create_location(location_use_cases: LocationUseCases = Depends(Provide[Container.location_use_cases])):
    location_use_cases.create_location()

    return "seeded successfully"
