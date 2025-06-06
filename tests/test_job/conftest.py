import pytest

from unittest.mock import Mock
from sqlalchemy.orm import Session

from domain.entities.job import Job
from domain.exceptions.not_found_error import NotFoundError
from domain.interfaces.job_repository_interface import JobRepositoryInterface
from domain.schemas.job_schema import JobSchemaCreate, JobSchemaUpdate
from interface_adapters.database.sqlalchemy.job_repository import SQLAlchemyJobRepository
from use_cases.job_use_cases import JobUseCases
from domain.exceptions.integrity_error import IntegrityError


@pytest.fixture
def mock_session():
    return Mock(spec=Session)


@pytest.fixture
def mock_job_repo_interface():
    return Mock(spec=JobRepositoryInterface)


@pytest.fixture
def mock_job_use_cases():
    return Mock(spec=JobUseCases)


@pytest.fixture
def mock_job_repo_success(
    mock_job_repo_interface,
    job_created,
    jobs,
    job_updated
):
    repo = mock_job_repo_interface
    repo.create_job.return_value = job_created
    repo.get_all_jobs.return_value = jobs
    repo.get_job_by_id.return_value = job_created
    repo.update_job.return_value = job_updated
    repo.delete_job.return_value = True

    return repo


@pytest.fixture
def mock_job_repo_failure(mock_session):
    repo = SQLAlchemyJobRepository(session=mock_session)
    repo.create_job = Mock(side_effect=IntegrityError("error"))
    repo.get_all_jobs = Mock(side_effect=NotFoundError("error"))
    repo.get_job_by_id = Mock(side_effect=NotFoundError("error"))
    repo.update_job = Mock(side_effect=IntegrityError("error"))
    repo.delete_job = Mock(side_effect=NotFoundError("error"))

    return repo


@pytest.fixture
def create_job_data():
    return JobSchemaCreate(
        name= "Test",
        application_date= "2025-06-03",
        outcome= "test",
        application_stage_id= 1,
        user_id= 1,
        company_id= 1,
        country_id= 1,
        state_id= 1,
        city_id= 1
    )


@pytest.fixture
def job_created(create_job_data):
    return Job(
        id= 1,
        name= create_job_data.name,
        link= None,
        application_date= create_job_data.application_date,
        application_stage_id= create_job_data.application_stage_id,
        outcome= create_job_data.outcome,
        user_id= create_job_data.user_id,
        company_id= create_job_data.company_id,
        country_id= create_job_data.country_id,
        state_id= create_job_data.state_id,
        city_id= create_job_data.city_id,
        created_at= "2025-06-06T17:35:35.863146",
        updated_at= None
    )


@pytest.fixture
def update_job_data():
    return JobSchemaUpdate(
        name= "Update",
        application_date= "2025-06-03",
        outcome= "Update",
        application_stage_id= 1,
        user_id= 1,
        company_id= 1,
        country_id= 1,
        state_id= 1,
        city_id= 1
    )


@pytest.fixture
def job_updated(update_job_data):
    return Job(
        id= 1,
        name= update_job_data.name,
        link= None,
        application_date= update_job_data.application_date,
        application_stage_id= update_job_data.application_stage_id,
        outcome= update_job_data.outcome,
        user_id= update_job_data.user_id,
        company_id= update_job_data.company_id,
        country_id= update_job_data.country_id,
        state_id= update_job_data.state_id,
        city_id= update_job_data.city_id,
        created_at= "2025-06-06T17:35:35.863146",
        updated_at= "2025-06-06T17:35:35.863146"
    )


@pytest.fixture
def jobs():
    return [
        Job(
            id= 1,
            name= "Test1",
            link= None,
            application_date= "2025-06-03",
            application_stage_id= 1,
            outcome= "Test1",
            user_id= 1,
            company_id= 1,
            country_id= 1,
            state_id= 1,
            city_id= 1,
            created_at= "2025-06-06T17:35:35.863146",
            updated_at= None
        ),
        Job(
            id= 2,
            name= "Test2",
            link= None,
            application_date= "2025-06-03",
            application_stage_id= 1,
            outcome= "Test2",
            user_id= 1,
            company_id= 1,
            country_id= 1,
            state_id= 1,
            city_id= 1,
            created_at= "2025-06-06T17:35:35.863146",
            updated_at= None
        ),
        Job(
            id= 3,
            name= "Test3",
            link= None,
            application_date= "2025-06-03",
            application_stage_id= 1,
            outcome= "Test3",
            user_id= 1,
            company_id= 1,
            country_id= 1,
            state_id= 1,
            city_id= 1,
            created_at= "2025-06-06T17:35:35.863146",
            updated_at= None
        ),
    ]
