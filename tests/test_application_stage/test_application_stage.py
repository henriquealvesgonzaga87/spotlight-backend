import pytest

from domain.entities.application_stage import ApplicationStage
from domain.exceptions.integrity_error import IntegrityError


class TestApplicationStage:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    @pytest.mark.asyncio
    async def test_create_application_stage_success(
        self,
        mock_application_stage_repo_success,
        create_application_stage_data,
    ):
        new_application_stage = await mock_application_stage_repo_success.create_application_stage(
            application_stage=create_application_stage_data
        )

        assert new_application_stage is not None
        assert new_application_stage.application_stage == create_application_stage_data.application_stage
        assert isinstance(new_application_stage, ApplicationStage)

    @pytest.mark.asyncio
    async def test_create_application_stage_failure(
        self,
        mock_application_stage_repo_failure,
        create_application_stage_data
    ):
        with pytest.raises(IntegrityError, match="Error"):
            await mock_application_stage_repo_failure.create_application_stage(
                application_stage=create_application_stage_data
            )
