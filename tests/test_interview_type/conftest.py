import pytest
from sqlalchemy.orm import Session
from unittest.mock import Mock

from domain.entities.interview_type import InterviewType
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError
from domain.interfaces.interview_type_repository_interface import InterviewTypeRepositoryInterface
from domain.schemas.interview_type_schema import InterviewTypeSchemaCreate
from interface_adapters.database.sqlalchemy.interview_type_repository import SQLAlchemyInterviewTypeRepository
from use_cases.interview_type_use_cases import InterviewTypeUseCases


@pytest.fixture
def mock_session():
    return Mock(spec=Session)


@pytest.fixture
def mock_interview_type_repo_interface():
    return Mock(spec=InterviewTypeRepositoryInterface)


@pytest.fixture
def mock_interview_type_use_cases():
    return Mock(spec=InterviewTypeUseCases)


@pytest.fixture
def mock_interview_type_repo_for_route_tests():
    repo = Mock()

    return repo


@pytest.fixture
def mock_interview_type_repo_success(
        mock_interview_type_repo_interface,
        interview_type_created,
        interview_types,
        interview_type_updated
    ):
    repo = mock_interview_type_repo_interface
    repo.create_interview_type.return_value = interview_type_created
    repo.get_all_interview_type.return_value = interview_types
    repo.get_interview_type_by_id.return_value = interview_type_created
    repo.update_interview_type.return_value = interview_type_updated
    repo.delete_interview_type.return_value = True

    return repo


@pytest.fixture
def mock_interview_type_repo_failure(mock_session):
    repo = SQLAlchemyInterviewTypeRepository(session=mock_session)
    repo.create_interview_type = Mock(side_effect=IntegrityError("error"))
    repo.get_all_interview_type = Mock(side_effect=NotFoundError("error"))
    repo.get_interview_type_by_id = Mock(side_effect=NotFoundError("error"))
    repo.update_interview_type = Mock(side_effect=IntegrityError("error"))
    repo.delete_interview_type = Mock(side_effect=NotFoundError("error"))

    return repo


@pytest.fixture
def create_interview_type_data():
    return InterviewTypeSchemaCreate(
        interview_type="Test"
    )


@pytest.fixture
def interview_type_created(create_interview_type_data):
    return InterviewType(
        id= 1,
        interview_type= create_interview_type_data.interview_type,
        created_at= "2025-06-07T10:25:56.830999",
        updated_at= None
    )


@pytest.fixture
def interview_types():
    return [
        InterviewType(
            id= 1,
            interview_type= "Test",
            created_at= "2025-06-07T10:25:56.830999",
            updated_at= None
        ),
        InterviewType(
            id= 2,
            interview_type= "Test dois",
            created_at= "2025-06-07T10:25:56.830999",
            updated_at= None
        ),
        InterviewType(
            id= 3,
            interview_type= "Test tres",
            created_at= "2025-06-07T10:25:56.830999",
            updated_at= None
        ),
    ]


@pytest.fixture
def update_interview_type_data():
    return InterviewTypeSchemaCreate(
        interview_type="Test updated"
    )


@pytest.fixture
def interview_type_updated(update_interview_type_data):
    return InterviewType(
        id= 1,
        interview_type= update_interview_type_data.interview_type,
        created_at= "2025-06-07T10:25:56.830999",
        updated_at= "2025-06-07T10:25:56.830999"
    )


@pytest.fixture
def interview_type_create_json_response():
    return {
        'id': 1, 
        'interview_type': 'Test', 
        'created_at': '2025-06-07T10:25:56.830999', 
        'updated_at': None
    }


@pytest.fixture
def interview_type_update_json_response():
    return {
        'id': 1, 
        'interview_type': 'Test updated', 
        'created_at': '2025-06-07T10:25:56.830999', 
        'updated_at': '2025-06-07T10:25:56.830999'
    }


@pytest.fixture
def interview_types_json_response():
    return [
        {
            'id': 1, 
            'interview_type': 'Test', 
            'created_at': '2025-06-07T10:25:56.830999', 
            'updated_at': None
        }, 
        {
             'id': 2, 
             'interview_type': 'Test dois', 
             'created_at': '2025-06-07T10:25:56.830999', 
             'updated_at': None
        }, 
        {
            'id': 3, 
            'interview_type': 'Test tres', 
            'created_at': '2025-06-07T10:25:56.830999', 
            'updated_at': None
        }
    ]
