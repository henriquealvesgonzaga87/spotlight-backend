from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide

from containers.container import Container
from domain.entities.location import City, Country
from domain.schemas.location_schema import CityCreateSchema, CitySchema, CountryCreateSchema, CountrySchema
from use_cases.location_use_cases import LocationUseCases


router = APIRouter()


@router.post("/location/country", status_code=status.HTTP_201_CREATED, response_model=CountrySchema)
@inject
def create_country(country_data: CountryCreateSchema, location_use_cases: LocationUseCases = Depends(Provide[Container.location_use_cases])):
    country = location_use_cases.create_country(
        country=Country(
            common_name=country_data.common_name
        )
    )

    country_json = jsonable_encoder(country)

    return country_json


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
