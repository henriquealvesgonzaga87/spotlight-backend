import pytest
from sqlalchemy.orm import Session
from unittest.mock import Mock

from domain.entities.user import User
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError
from domain.interfaces.user_repository_interface import UserRepositoryInterface
from domain.schemas.user_schema import UserSchemaCreate
from interface_adapters.database.sqlalchemy.user_repository import SQLAlchemyUserRepository
from use_cases.user_use_cases import UserUseCases


@pytest.fixture
def mock_session():
    return Mock(spec=Session)


@pytest.fixture
def mock_user_repo_interface():
    user_repo_interface = Mock(spec=UserRepositoryInterface)

    return user_repo_interface


@pytest.fixture
def mock_user_use_cases():
    user_use_cases = Mock(spec=UserUseCases)

    return user_use_cases


@pytest.fixture
def mock_user_repository_for_route_tests(user_created):
    user_repository = Mock()
    user_repository.create_user = Mock(return_value=user_created)
    user_repository.get_user_by_id = Mock(return_value=user_created)
    return user_repository


@pytest.fixture
def mock_user_repo_interface_success(mock_user_repo_interface, user_created, user_updated):
    user_repo_interface = mock_user_repo_interface
    user_repo_interface.create_user.return_value = user_created
    user_repo_interface.get_user_by_id.return_value = user_created
    user_repo_interface.update_user.return_value = user_updated
    user_repo_interface.delete_user.return_value = True

    return user_repo_interface


@pytest.fixture
def mock_user_repo_failure(mock_session):
    user_repo = SQLAlchemyUserRepository(session=mock_session)
    user_repo.create_user = Mock(side_effect=IntegrityError("Integrity error occurred"))
    user_repo.get_user_by_id = Mock(side_effect=NotFoundError("Not found with the given parameter"))
    user_repo.update_user = Mock(side_effect=Exception("Not found with the given parameter"))
    user_repo.delete_user = Mock(side_effect=Exception("Not found with the given parameter"))
    return user_repo


@pytest.fixture
def create_user_data():
    return UserSchemaCreate(
        name='Test',
        email='test@mail.com',
        password='test'
    )


@pytest.fixture
def update_user_data():
    return UserSchemaCreate(
        name='Test Updated',
        email='testupdated@mail.com',
        password='testupdated'
    )


@pytest.fixture
def user_created(create_user_data):
    return User(
        id=0,
        name=create_user_data.name,
        email=create_user_data.email,
        password=create_user_data.password,
        created_at="2025-04-24 20:29:20.461333",
        updated_at=None,
    )


@pytest.fixture
def user_updated(user_created, update_user_data):
    return User(
        id=user_created.id,
        name=update_user_data.name,
        email=update_user_data.email,
        password=update_user_data.password,
        created_at="2025-04-24 20:29:20.461333",
        updated_at="2025-04-24 20:29:20.461333",
    )


@pytest.fixture
def user_id_data():
    return 0
