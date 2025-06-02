import pytest

from unittest.mock import Mock
from sqlalchemy.orm import Session

from domain.entities.application_stage import ApplicationStage
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError
from domain.interfaces.application_stage_repository_interface import ApplicationStageRepositoryInterface
from domain.schemas.application_stage_schema import ApplicationStageSchemaCreate
from interface_adapters.database.sqlalchemy.application_stage_repository import SQLAlchemyApplicationStageRepository
from use_cases.application_stage_use_cases import ApplicationStageUseCases


@pytest.fixture
def mock_session():
    return Mock(spec=Session)


@pytest.fixture
def mock_application_stage_repo_interface():
    application_stage_repo_interface = Mock(spec=ApplicationStageRepositoryInterface)

    return application_stage_repo_interface


@pytest.fixture
def mock_application_stage_use_cases():
    application_stage_use_cases = Mock(spec=ApplicationStageUseCases)

    return application_stage_use_cases


@pytest.fixture
def mock_application_stage_repo_success(
    mock_application_stage_repo_interface,
    application_stage_created,
    applications_stage,
):
    application_stage_repo = mock_application_stage_repo_interface
    application_stage_repo.create_application_stage.return_value = application_stage_created
    application_stage_repo.get_all_application_stage.return_value = applications_stage
    application_stage_repo.get_application_stage_by_id.return_value = application_stage_created


    return application_stage_repo


@pytest.fixture
def mock_application_stage_repo_failure(mock_session):
    repo = SQLAlchemyApplicationStageRepository(session=mock_session)
    repo.create_application_stage = Mock(side_effect=IntegrityError("Error"))
    repo.get_all_application_stage = Mock(side_effect=NotFoundError("Error"))
    repo.get_application_stage_by_id = Mock(side_effect=NotFoundError("Error"))

    return repo


@pytest.fixture
def create_application_stage_data():
    return ApplicationStageSchemaCreate(
        application_stage="Test"
    )


@pytest.fixture
def update_application_stage_data():
    return ApplicationStageSchemaCreate(
        application_stage="Test updated"
    )


@pytest.fixture
def application_stage_created(create_application_stage_data):
    return ApplicationStage(
        id=1,
        application_stage=create_application_stage_data.application_stage,
        created_at="2025-04-24 20:29:20.461333",
        updated_at=None
    )


@pytest.fixture
def application_stage_updated(update_application_stage_data, application_stage_created):
    return ApplicationStage(
        id=application_stage_created.id,
        application_stage=update_application_stage_data.application_stage,
        created_at="2025-04-24 20:29:20.461333",
        updated_at="2025-04-24 20:29:20.461333"
    )


@pytest.fixture
def applications_stage():
    return [
        ApplicationStage(
            id=1,
            application_stage="Test",
            created_at="2025-04-24 20:29:20.461333",
            updated_at=None
        ),
        ApplicationStage(
            id=2,
            application_stage="Test second",
            created_at="2025-04-24 20:29:20.461333",
            updated_at=None
        ),
        ApplicationStage(
            id=3,
            application_stage="Test third",
            created_at="2025-04-24 20:29:20.461333",
            updated_at=None
        ),
    ]
