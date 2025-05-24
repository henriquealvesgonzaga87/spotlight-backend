from fastapi import APIRouter, status, Depends, Body
from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide

from containers.container import Container
from domain.entities.location import City, State
from domain.schemas.location_schema import CityCreateSchema, CitySchema, CountrySchema, GetCitiesSchema, StateCreateSchema, StateSchema
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
def get_country_by_id(country_id: int, location_use_cases: LocationUseCases = Depends(Provide[Container.location_use_cases])):
    country = location_use_cases.get_country_by_id(country_id=country_id)

    country_json = jsonable_encoder(country)

    return country_json


@router.get("/location/country/state/{country_name}", status_code=status.HTTP_200_OK, response_model=list[StateSchema])
@inject
def get_states(country_name: str, location_use_cases: LocationUseCases = Depends(Provide[Container.location_use_cases])):
    states = location_use_cases.get_states(country_name=country_name)

    states_json = jsonable_encoder(states)

    return states_json


@router.get("/location/state/{state_id}", status_code=status.HTTP_200_OK, response_model=StateSchema)
@inject
def get_state_by_id(state_id: int, location_use_cases: LocationUseCases = Depends(Provide[Container.location_use_cases])):
    state = location_use_cases.get_state_by_id(state_id=state_id)

    state_json = jsonable_encoder(state)

    return state_json


@router.post("/location/state/", status_code=status.HTTP_201_CREATED, response_model=StateSchema)
@inject
def create_state(state_data: StateCreateSchema = Body(...), location_use_cases: LocationUseCases = Depends(Provide[Container.location_use_cases])):
    state = location_use_cases.create_state(
        state=State(
            name=state_data.name,
            country_id=state_data.country_id
        )
    )

    state_json = jsonable_encoder(state)

    return state_json


@router.post("/location/city/{country_name}/{state_name}", status_code=status.HTTP_201_CREATED, response_model=CitySchema)
@inject
def create_city(country_name: str, state_name: str, city_data: CityCreateSchema = Body(...), location_use_case: LocationUseCases = Depends(Provide[Container.location_use_cases])):
    city = location_use_case.create_city(city=City(
        name=city_data.name,
        ),
        country_name=country_name,
        state_name=state_name
    )

    city_json = jsonable_encoder(obj=city)

    return city_json


@router.get("/location/city", status_code=status.HTTP_200_OK, response_model=list[CitySchema])
@inject
def get_cities(get_cities_body: GetCitiesSchema = Body(...), location_use_case: LocationUseCases = Depends(Provide[Container.location_use_cases])):
    cities = location_use_case.get_cities(
        country_name=get_cities_body.country_name,
        state_name=get_cities_body.state_name
    )

    cities_json = jsonable_encoder(cities)

    return cities_json


@router.get("/location/city/{city_id}", status_code=status.HTTP_200_OK, response_model=CitySchema)
@inject
def get_city_by_id(city_id: int, location_use_case: LocationUseCases = Depends(Provide[Container.location_use_cases])):
    city = location_use_case.get_city_by_id(city_id=city_id)

    city_json = jsonable_encoder(city)

    return city_json
