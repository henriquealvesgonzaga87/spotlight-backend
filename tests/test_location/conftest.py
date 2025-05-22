import os
import pytest

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from unittest.mock import Mock

from domain.entities.location import City, Country, State
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError
from domain.interfaces.location_repository_interface import LocationRepositoryInterface
from domain.schemas.location_schema import CityCreateSchema, StateCreateSchema
from interface_adapters.database.sqlalchemy.location_repository import SQLAlchemyLocationRepository
from use_cases.location_use_cases import LocationUseCases


load_dotenv()


@pytest.fixture
def mock_session():
    return Mock(spec=Session)


@pytest.fixture
def mock_location_repo_interface():
    return Mock(spec=LocationRepositoryInterface)


@pytest.fixture
def mock_location_use_cases():
    return Mock(spec=LocationUseCases)


@pytest.fixture
def api_geonames_connection_string_success():
    return os.getenv("API_COUNTRIES")


@pytest.fixture
def api_geonames_connection_string_failure():
    return "http://api.geonames.org/countryInfoJSON?username=testfailure"


@pytest.fixture
def mock_location_repo_success(
    mock_location_repo_interface, 
    countries, 
    country,
    states,
    state,
    city,
    cities
    ):
    location_repo = mock_location_repo_interface
    location_repo.create_country.return_value = countries
    location_repo.get_countries.return_value = countries
    location_repo.get_country_by_id.return_value = country
    location_repo.get_states.return_value = states
    location_repo.get_state_by_id.return_value = state
    location_repo.create_state.return_value = state
    location_repo.create_city.return_value = city
    location_repo.get_cities.return_value = cities

    return location_repo


@pytest.fixture
def mock_location_repo_failure(mock_session):
    location_repo = SQLAlchemyLocationRepository(session=mock_session)
    location_repo.create_country = Mock(side_effect=IntegrityError("!!!ERROR"))
    location_repo._filter_location = Mock(side_effect=NotFoundError("ERROR"))
    location_repo.get_countries = Mock(side_effect=NotFoundError("Not found"))
    location_repo.get_country_by_id = Mock(side_effect=NotFoundError("Not found"))
    location_repo.get_states = Mock(side_effect=NotFoundError("Not found"))
    location_repo.get_state_by_id = Mock(side_effect=NotFoundError("Not found"))
    location_repo.create_state = Mock(side_effect=IntegrityError("Error"))
    location_repo.create_city = Mock(side_effect=IntegrityError("Error"))
    location_repo.get_cities = Mock(side_effect=NotFoundError("Not found"))

    return location_repo


@pytest.fixture
def countries():
    return [
        Country(
            id=0,
            common_name="Andorra",
            code="AD"
        ),
        Country(
            id=1,
            common_name="United Arab Emirates",
            code="AE"
        ),
        Country(
            id=2,
            common_name="Afghanistan",
            code="AF"
        )
    ]


@pytest.fixture
def country():
    return  Country(
        id=0,
        common_name="Andorra",
        code="AD"
    )


@pytest.fixture
def states():
    return [
        State(
            id=0,
            name="Escaldes-Engordany",
            code="08",
            admin_code=8,
            country_id=1
        ),
        State(
            id=1,
            name="Sant Julià de Loria",
            code="06",
            admin_code=6,
            country_id=1
        ),
        State(
            id=2,
            name="Ordino",
            code="05",
            admin_code=5,
            country_id=1
        )
    ]


@pytest.fixture
def state():
    return State(
        id=0,
        name="Escaldes-Engordany",
        code="08",
        admin_code=8,
        country_id=1
    )


@pytest.fixture
def cities():
    return [
        City(
            id= 0,
            name="Les Escaldes",
            state_id=1
        ),
        City(
            id= 1,
            name="Els Vilars",
            state_id=1
        ),
        City(
            id= 2,
            name="Engordany",
            state_id=1
        )
    ]


@pytest.fixture
def city():
    return City(
        id= 0,
        name="Les Escaldes",
        state_id=1
    )


@pytest.fixture
def create_state_data():
    return StateCreateSchema(
        name="Escaldes-Engordany",
        country_id=1
    )


@pytest.fixture
def create_city_data():
    return CityCreateSchema(
        name="Les Escaldes"
    )
