import os
import pytest

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from unittest.mock import Mock

from domain.entities.location import Country
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError
from domain.interfaces.location_repository_interface import LocationRepositoryInterface
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
def mock_location_repo_success(mock_location_repo_interface, countries, country):
    location_repo = mock_location_repo_interface
    location_repo.create_country.return_value = countries

    return location_repo


@pytest.fixture
def mock_location_repo_failure(mock_session):
    location_repo = SQLAlchemyLocationRepository(session=mock_session)
    location_repo.create_country = Mock(side_effect=IntegrityError("!!!ERROR"))
    location_repo._filter_location = Mock(side_effect=NotFoundError("ERROR"))

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
