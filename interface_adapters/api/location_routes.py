from fastapi import APIRouter, status, Depends, Body
from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide

from containers.container import Container
from domain.entities.location import City, Country, State
from domain.schemas.location_schema import CityCreateSchema, CitySchema, CountryCreateSchema, CountrySchema, StateCreateSchema, StateSchema
from use_cases.location_use_cases import LocationUseCases


router = APIRouter()


@router.post("/location/country", status_code=status.HTTP_201_CREATED)
@inject
def create_country(location_use_cases: LocationUseCases = Depends(Provide[Container.location_use_cases])):
    location_use_cases.create_country()

    return "Countries created successfully"


@router.get("/location/country", status_code=status.HTTP_200_OK, response_model=list[CountrySchema])
@inject
def get_countries(location_use_cases: LocationUseCases = Depends(Provide[Container.location_use_cases])):
    countries = location_use_cases.get_countries()

    countries_json = jsonable_encoder(countries)

    return countries_json


@router.get("/location/country/{country_id}", status_code=status.HTTP_200_OK, response_model=CountrySchema)
@inject
def get_country_by_id(country_id: int, location_use_cases = Depends(Provide[Container.location_use_cases])):
    country = location_use_cases.get_country_by_id(country_id=country_id)

    country_json = jsonable_encoder(country)

    return country_json


@router.get("/location/state/{country_name}", status_code=status.HTTP_200_OK, response_model=list[StateSchema])
@inject
def get_states(country_name: str, location_use_cases = Depends(Provide[Container.location_use_cases])):
    states = location_use_cases.get_states(country_name=country_name)

    states_json = jsonable_encoder(states)

    return states_json


@router.post("/location/state/{country_name}", status_code=status.HTTP_201_CREATED, response_model=StateSchema)
@inject
def create_state(country_name: str, state_data: StateCreateSchema = Body(...), location_use_cases: LocationUseCases = Depends(Provide[Container.location_use_cases])):
    state = location_use_cases.create_state(
        state=State(
            name=state_data.name,
            country_id=state_data.country_id
        ),
        country_name=country_name,
    )

    state_json = jsonable_encoder(state)

    return state_json


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
