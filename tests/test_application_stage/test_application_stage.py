import pytest

from domain.entities.application_stage import ApplicationStage
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError


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

    @pytest.mark.asyncio
    async def test_get_all_application_stage_success(
        self,
        mock_application_stage_repo_success
    ):
        applications_stage = await mock_application_stage_repo_success.get_all_application_stage()

        assert len(applications_stage) != 0
        assert isinstance(applications_stage[0], ApplicationStage)
        assert isinstance(applications_stage[1], ApplicationStage)
        assert isinstance(applications_stage[2], ApplicationStage)

    @pytest.mark.asyncio
    async def test_get_all_application_stage_failure(
        self,
        mock_application_stage_repo_failure
    ):
        with pytest.raises(NotFoundError, match="Error"):
            mock_application_stage_repo_failure.get_all_application_stage()

    @pytest.mark.asyncio
    async def test_get_application_stage_by_id_success(
        self,
        mock_application_stage_repo_success,
        application_stage_id=1
    ):
        application_stage = await mock_application_stage_repo_success.get_application_stage_by_id(
            application_stage_id=application_stage_id
        )

        assert application_stage is not None
        assert application_stage.id == application_stage_id
        assert isinstance(application_stage, ApplicationStage)

    @pytest.mark.asyncio
    async def test_get_application_stage_by_id_failure(
        self,
        mock_application_stage_repo_failure,
        application_stage_id=99
    ):
        with pytest.raises(NotFoundError, match="Error"):
            mock_application_stage_repo_failure.get_application_stage_by_id(
                application_stage_id=application_stage_id
            )

    @pytest.mark.asyncio
    async def test_update_application_stage_success(
        self,
        mock_application_stage_repo_success,
        update_application_stage_data,
        application_stage_id=1
    ):
        application_stage = await mock_application_stage_repo_success.update_application_stage(
            application_stage=update_application_stage_data,
            application_stage_id=application_stage_id
        )

        assert application_stage is not None
        assert application_stage.id == application_stage_id
        assert isinstance(application_stage, ApplicationStage)

    @pytest.mark.asyncio
    async def test_update_application_stage_failure(
        self,
        mock_application_stage_repo_failure,
        update_application_stage_data,
        application_stage_id=99
    ):
        with pytest.raises(IntegrityError, match="Error"):
            await mock_application_stage_repo_failure.update_application_stage(
            application_stage=update_application_stage_data,
            application_stage_id=application_stage_id
        )
            
    @pytest.mark.asyncio
    async def test_delete_application_stage_success(
        self,
        mock_application_stage_repo_success,
        application_stage_id=1
    ):
        application_stage = await mock_application_stage_repo_success.delete_application_stage(
            application_stage_id=application_stage_id
        )

        assert application_stage is True

    @pytest.mark.asyncio
    async def test_delete_application_stage_failure(
        self,
        mock_application_stage_repo_failure,
        application_stage_id=99
    ):
        with pytest.raises(NotFoundError, match="Error"):
            await mock_application_stage_repo_failure.delete_application_stage(
            application_stage_id=application_stage_id
        )
