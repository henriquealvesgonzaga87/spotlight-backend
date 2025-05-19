import pytest
from sqlalchemy.orm import Session
from unittest.mock import Mock

from domain.entities.location import Country
from domain.interfaces.location_repository_interface import LocationRepositoryInterface
from domain.schemas.location_schema import CountryCreateSchema
from use_cases.location_use_cases import LocationUseCases


@pytest.fixture
def mcok_session():
    return Mock(spec=Session)


@pytest.fixture
def mock_location_repo_interface():
    return Mock(spec=LocationRepositoryInterface)


@pytest.fixture
def mock_location_use_cases():
    return Mock(spec=LocationUseCases)


@pytest.fixture
def mock_location_repo_success(mock_location_repo_interface, countries):
    location_repo = mock_location_repo_interface
    location_repo.create_country.return_value = countries

    return location_repo


@pytest.fixture
def mock_location_repo_failure(mock_location_repo_interface):
    location_repo = mock_location_repo_interface

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
