import pytest
from sqlalchemy.orm import Session
from unittest.mock import Mock

from domain.entities.interview import Interview
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError
from domain.interfaces.interview_repository_interface import InterviewRepositoryInterface
from domain.schemas.interview_schema import InterviewSchemaCreate, InterviewSchemaUpdate
from interface_adapters.database.sqlalchemy.interview_repository import SQLAlchemyInterviewRepository
from use_cases.interview_use_cases import InterviewUseCases


@pytest.fixture
def mock_session():
    return Mock(spec=Session)


@pytest.fixture
def mock_interview_repo_interface():
    return Mock(spec=InterviewRepositoryInterface)


@pytest.fixture
def mock_interview_use_cases():
    return Mock(spec=InterviewUseCases)


@pytest.fixture
def mock_interview_repo_for_route_tests():
    repo = Mock()

    return repo


@pytest.fixture
def mock_interview_repo_success(
    mock_interview_repo_interface,
    interview_created,
    interviews,
    interview_updated
):
    repo = mock_interview_repo_interface
    repo.create_interview.return_value = interview_created
    repo.get_all_interview.return_value = interviews
    repo.get_interview_by_id.return_value = interview_created
    repo.update_interview.return_value = interview_updated
    repo.delete_interview.return_value = True

    return repo


@pytest.fixture
def mock_interview_repo_failure(mock_session):
    repo = SQLAlchemyInterviewRepository(session=mock_session)
    repo.create_interview = Mock(side_effect=IntegrityError("error"))
    repo.get_all_interview = Mock(side_effect=NotFoundError("error"))
    repo.get_interview_by_id = Mock(side_effect=NotFoundError("error"))
    repo.update_interview = Mock(side_effect=IntegrityError("error"))
    repo.delete_interview = Mock(side_effect=IntegrityError("error"))

    return repo


@pytest.fixture
def create_interview_data():
    return InterviewSchemaCreate(
        result= "test",
        interview_date= "2025-06-07 12:30",
        interview_type_id= 1,
        job_id= 1
    )


@pytest.fixture
def interview_created(create_interview_data):
    return Interview(
        id= 1,
        result= create_interview_data.result,
        interview_date= create_interview_data.interview_date,
        interview_type_id= create_interview_data.interview_type_id,
        job_id= create_interview_data.job_id,
        created_at= "2025-06-07T14:36:49.808210",
        updated_at= None
    )


@pytest.fixture
def update_interview_data():
    return InterviewSchemaUpdate(
        result= "test updated",
        interview_date= "2025-06-08 12:30",
        interview_type_id= 1,
        job_id= 1
    )


@pytest.fixture
def interview_updated(update_interview_data, interview_created):
    return Interview(
        id= interview_created.id,
        result= update_interview_data.result,
        interview_date= update_interview_data.interview_date,
        interview_type_id= update_interview_data.interview_type_id,
        job_id= update_interview_data.job_id,
        created_at= "2025-06-07T14:36:49.808210",
        updated_at= "2025-06-07T14:36:49.808210"
    )


@pytest.fixture
def interviews():
    return [
        Interview(
            id= 1,
            result= "Test",
            interview_date= "2025-06-12T10:00:00",
            interview_type_id= 1,
            job_id= 1,
            created_at= "2025-06-07T14:36:49.808210",
            updated_at= None
        ),
        Interview(
            id= 2,
            result= "Test2",
            interview_date= "2025-06-12T10:00:00",
            interview_type_id= 1,
            job_id= 1,
            created_at= "2025-06-07T14:36:49.808210",
            updated_at= None
        ),
        Interview(
            id= 3,
            result= "Test3",
            interview_date= "2025-06-12T10:00:00",
            interview_type_id= 1,
            job_id= 1,
            created_at= "2025-06-07T14:36:49.808210",
            updated_at= None
        ),
    ]


@pytest.fixture
def create_interview_json_response():
    return {
        'id': 1, 
        'result': 'test', 
        'interview_date': '2025-06-07T12:30:00', 
        'interview_type_id': 1, 
        'job_id': 1, 
        'created_at': '2025-06-07T14:36:49.808210', 
        'updated_at': None
    }


@pytest.fixture
def update_interview_json_response():
    return {
        'id': 1, 
        'result': 'test updated', 
        'interview_date': '2025-06-08T12:30:00', 
        'interview_type_id': 1, 
        'job_id': 1, 
        'created_at': '2025-06-07T14:36:49.808210', 
        'updated_at': '2025-06-07T14:36:49.808210'
    }


@pytest.fixture
def get_all_interviews_json_response():
    return [
        {
            'id': 1, 
            'result': 'Test', 
            'interview_date': '2025-06-12T10:00:00', 
            'interview_type_id': 1, 'job_id': 1, 
            'created_at': '2025-06-07T14:36:49.808210', 
            'updated_at': None
        }, 
        {
            'id': 2, 
            'result': 'Test2', 
            'interview_date': '2025-06-12T10:00:00', 
            'interview_type_id': 1, 
            'job_id': 1, 
            'created_at': '2025-06-07T14:36:49.808210', 
            'updated_at': None
        }, 
        {
            'id': 3, 
            'result': 'Test3', 
            'interview_date': '2025-06-12T10:00:00', 
            'interview_type_id': 1, 
            'job_id': 1, 
            'created_at': '2025-06-07T14:36:49.808210', 
            'updated_at': None
        }
    ]
