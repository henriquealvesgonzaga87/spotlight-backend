import os
import pytest

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from unittest.mock import Mock
from datetime import datetime, timedelta
from jose import jwt

from domain.entities.company import Company
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError
from domain.interfaces.company_repository_interface import CompanyRepositoryInterface
from domain.schemas.company_schema import CompanySchemaCreate
from interface_adapters.database.sqlalchemy.company_repository import SQLAlchemyCompanyRepository
from use_cases.company_use_cases import CompanyUseCases
from domain.schemas.auth_schema import LoginSchema


load_dotenv(".env.test")


@pytest.fixture
def mock_session():
    return Mock(spec=Session)


@pytest.fixture
def mock_company_repo_interface():
    company_repo_interface = Mock(spec=CompanyRepositoryInterface)

    return company_repo_interface


@pytest.fixture
def mock_company_use_cases():
    company_use_cases = Mock(spec=CompanyUseCases)

    return company_use_cases


@pytest.fixture
def mock_company_repository_for_route_tests(company_created):
    company_repository = Mock()
    company_repository.create_company = Mock(return_value=company_created)

    return company_repository


@pytest.fixture
def mock_company_repo_interface_success(mock_company_repo_interface, company_created, companies, company_updated):
    company_repo_interface = mock_company_repo_interface
    company_repo_interface.create_company.return_value = company_created
    company_repo_interface.get_company_by_id.return_value = company_created
    company_repo_interface.get_all_companies.return_value = companies
    company_repo_interface.update_company.return_value = company_updated
    company_repo_interface.delete_company.return_value = True

    return company_repo_interface


@pytest.fixture
def mock_company_repo_interface_failure(mock_session):
    company_repo = SQLAlchemyCompanyRepository(session=mock_session)
    company_repo.create_company = Mock(side_effect=IntegrityError("Integrity error: duplicate entry or constraint violation."))
    company_repo.get_company_by_id = Mock(side_effect=NotFoundError("Not found with the given parameter"))
    company_repo.get_all_companies = Mock(side_effect=NotFoundError("There's no data to show"))
    company_repo.update_company = Mock(side_effect=IntegrityError("Integrity error: duplicate entry or constraint violation."))
    company_repo.delete_company = Mock(side_effect=NotFoundError("Not found with the given parameter"))

    return company_repo


@pytest.fixture
def create_company_data():
    return CompanySchemaCreate(
        name='Test',
        link="https://www.test.com"
    )


@pytest.fixture
def update_company_data():
    return CompanySchemaCreate(
        name='Test Updated',
        link="https://www.testupdated.com"
    )


@pytest.fixture
def company_created(create_company_data):
    return Company(
        id=0,
        name=create_company_data.name,
        link=create_company_data.link,
        created_at="2025-04-24 20:29:20.461333",
        updated_at=None,
    )


@pytest.fixture
def company_updated(company_created, update_company_data):
    return Company(
        id=company_created.id,
        name=update_company_data.name,
        link=update_company_data.link,
        created_at="2025-04-24 20:29:20.461333",
        updated_at="2025-04-24 20:29:20.461333",
    )


@pytest.fixture
def companies():
    return [
        Company(
            id=0,
            name="Test",
            link="https://www.test.com",
            created_at="2025-04-24 20:29:20.461333",
            updated_at=None,
        ),
        Company(
            id=1,
            name="Test One",
            link="https://www.test.com",
            created_at="2025-04-24 20:29:20.461333",
            updated_at=None,
        ),
        Company(
            id=2,
            name="Test Two",
            link="https://www.test.com",
            created_at="2025-04-24 20:29:20.461333",
            updated_at=None,
        ),
    ]
