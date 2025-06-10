import pytest

from domain.entities.interview import Interview
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError


class TestInterview:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    @pytest.mark.asyncio
    async def test_create_interview_success(
        self,
        mock_interview_repo_success,
        create_interview_data
    ):
        new_interview = await mock_interview_repo_success.create_interview(
            interview=create_interview_data
        )

        assert new_interview is not None
        assert new_interview.result == create_interview_data.result
        assert new_interview.interview_date == create_interview_data.interview_date
        assert new_interview.interview_type_id == create_interview_data.interview_type_id
        assert new_interview.job_id == create_interview_data.job_id
        assert isinstance(new_interview, Interview)

    @pytest.mark.asyncio
    async def test_create_interview_failure(
        self,
        mock_interview_repo_failure,
        create_interview_data
    ):
        with pytest.raises(IntegrityError, match="error"):
            mock_interview_repo_failure.create_interview(
                interview=create_interview_data
            )

    @pytest.mark.asyncio
    async def test_get_all_interview_success(
        self,
        mock_interview_repo_success
    ):
        interviews = await mock_interview_repo_success.get_all_interview()

        assert len(interviews) > 0
        assert isinstance(interviews[0], Interview)
        assert isinstance(interviews[1], Interview)
        assert isinstance(interviews[2], Interview)

    @pytest.mark.asyncio
    async def test_get_all_interview_failure(
        self,
        mock_interview_repo_failure
    ):
        with pytest.raises(NotFoundError, match="error"):
            mock_interview_repo_failure.get_all_interview()

    @pytest.mark.asyncio
    async def test_get_interview_by_id_success(
        self,
        mock_interview_repo_success,
        interview_id=1
    ):
        interview = await mock_interview_repo_success.get_interview_by_id(
            interview_id=interview_id
        )

        assert interview is not None
        assert interview.id == interview_id
        assert isinstance(interview, Interview)

    @pytest.mark.asyncio
    async def test_get_interview_by_id_failure(
        self,
        mock_interview_repo_failure,
        interview_id=99
    ):
        with pytest.raises(NotFoundError, match="error"):
            mock_interview_repo_failure.get_interview_by_id(
                interview_id=interview_id
            )

    @pytest.mark.asyncio
    async def test_update_interview_success(
        self,
        mock_interview_repo_success,
        update_interview_data,
        interview_id=1
    ):
        updated_interview = await mock_interview_repo_success.update_interview(
            interview_id=interview_id,
            interview=update_interview_data
        )

        assert updated_interview is not None
        assert updated_interview.id == interview_id
        assert updated_interview.result == update_interview_data.result
        assert updated_interview.interview_date == update_interview_data.interview_date
        assert updated_interview.interview_type_id == update_interview_data.interview_type_id
        assert updated_interview.job_id == update_interview_data.job_id
        assert isinstance(updated_interview, Interview)

    @pytest.mark.asyncio
    async def test_update_interview_failure(
        self,
        mock_interview_repo_failure,
        update_interview_data,
        interview_id=99
    ):
        with pytest.raises(IntegrityError, match="error"):
            mock_interview_repo_failure.update_interview(
                interview_id=interview_id,
                interview=update_interview_data
            )

    @pytest.mark.asyncio
    async def test_delete_interview_success(
        self,
        mock_interview_repo_success,
        interview_id=1
    ):
        deleted_interview = await mock_interview_repo_success.delete_interview(
            interview_id=interview_id
        )

        assert deleted_interview is True
    
    @pytest.mark.asyncio
    async def test_delete_interview_failure(
        self,
        mock_interview_repo_failure,
        interview_id=99
    ):
        with pytest.raises(IntegrityError, match="error"):
            mock_interview_repo_failure.delete_interview(
                interview_id=interview_id
            )
