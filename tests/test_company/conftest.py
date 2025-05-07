import pytest
from sqlalchemy.orm import Session
from unittest.mock import Mock

from domain.entities.company import Company
from domain.exceptions.integrity_error import IntegrityError
from domain.interfaces.company_repository_interface import CompanyRepositoryInterface
from domain.schemas.company_schema import CompanySchemaCreate
from interface_adapters.database.sqlalchemy.company_repository import SQLAlchemyCompanyRepository
from use_cases.company_use_cases import CompanyUseCases


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
def mock_company_repo_interface_success(mock_company_repo_interface, company_created):
    company_repo_interface = mock_company_repo_interface
    company_repo_interface.create_company.return_value = company_created

    return company_repo_interface


@pytest.fixture
def mock_company_repo_interface_failure(mock_session):
    company_repo = SQLAlchemyCompanyRepository(session=mock_session)
    company_repo.create_company = Mock(side_effect=IntegrityError("Integrity error: duplicate entry or constraint violation."))

    return company_repo


@pytest.fixture
def create_company_data():
    return CompanySchemaCreate(
        name='Test',
        link="https://www.test.com"
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
