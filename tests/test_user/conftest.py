from sqlalchemy.orm import Session
from unittest.mock import Mock
import pytest

from domain.entities.user import User
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError
from domain.interfaces.user_repository_interface import UserRepositoryInterface
from domain.schemas.user_schema import UserSchemaCreate, UserSchema
from interface_adapters.database.sqlalchemy.user_repository import SQLAlchemyUserRepository


@pytest.fixture
def mock_session():
    return Mock(spec=Session)


@pytest.fixture
def mock_user_repo_interface():
    user_repo_interface = Mock(spec=UserRepositoryInterface)

    return user_repo_interface


@pytest.fixture
def mock_user_repo_interface_success(mock_user_repo_interface, user):
    user_repo_interface = mock_user_repo_interface
    user_repo_interface.create_user.return_value = user
    user_repo_interface.get_user_by_id.return_value = user

    return user_repo_interface


@pytest.fixture
def mock_user_repo_failure(mock_session):
    user_repo = SQLAlchemyUserRepository(session=mock_session)
    user_repo.create_user = Mock(side_effect=IntegrityError("Integrity error occurred"))
    user_repo.get_user_by_id = Mock(side_effect=NotFoundError("Not found with the given parameter"))
    return user_repo


@pytest.fixture
def create_user_data():
    return UserSchemaCreate(
        name='Test',
        email='test@mail.com',
        password='test'
    )


@pytest.fixture
def user():
    return User(
        id=0,
        name='Test',
        email='test@mail.com',
        password='test'
    )


@pytest.fixture
def user_id_data():
    return 0
