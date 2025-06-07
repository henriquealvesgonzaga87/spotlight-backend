import pytest
from unittest.mock import Mock

from domain.entities.interview_type import InterviewType
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError


class TestInterviewType:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    @pytest.mark.asyncio
    async def test_create_interview_type_success(
        self,
        mock_interview_type_repo_success, 
        create_interview_type_data
    ):
        new_interview_type = await mock_interview_type_repo_success.create_interview_type(
            interview_type=create_interview_type_data
        )

        assert new_interview_type is not None
        assert new_interview_type.interview_type == create_interview_type_data.interview_type
        assert isinstance(new_interview_type, InterviewType)

    @pytest.mark.asyncio
    async def test_create_interview_type_failure(
        self,
        mock_interview_type_repo_failure,
        create_interview_type_data
    ):
        with pytest.raises(IntegrityError, match="error"):
            mock_interview_type_repo_failure.create_interview_type(
                interview_type=create_interview_type_data
            )

    @pytest.mark.asyncio
    async def test_get_all_interview_type_success(
        self,
        mock_interview_type_repo_success
    ):
        interview_types = await mock_interview_type_repo_success.get_all_interview_type()

        assert len(interview_types) > 0
        assert isinstance(interview_types[0], InterviewType)
        assert isinstance(interview_types[1], InterviewType)
        assert isinstance(interview_types[2], InterviewType)

    @pytest.mark.asyncio
    async def test_get_all_interview_type_failure(
        self,
        mock_interview_type_repo_failure
    ):
        with pytest.raises(NotFoundError, match="error"):
            mock_interview_type_repo_failure.get_all_interview_type()

    @pytest.mark.asyncio
    async def test_get_interview_type_by_id_success(
        self,
        mock_interview_type_repo_success,
        interview_type_id=1
    ):
        interview_type = await mock_interview_type_repo_success.get_interview_type_by_id(
            interview_type_id=interview_type_id
        )

        assert interview_type is not None
        assert interview_type.id == interview_type_id
        assert isinstance(interview_type, InterviewType)

    @pytest.mark.asyncio
    async def test_get_interview_type_by_id_failure(
        self,
        mock_interview_type_repo_failure,
        interview_type_id=99
    ):
        with pytest.raises(NotFoundError, match="error"):
            mock_interview_type_repo_failure.get_interview_type_by_id(
                interview_type_id=interview_type_id
            )

    @pytest.mark.asyncio
    async def test_update_interview_type_success(
        self,
        mock_interview_type_repo_success,
        update_interview_type_data,
        interview_type_id=1
    ):
        interview_type = await mock_interview_type_repo_success.update_interview_type(
            interview_type_id=interview_type_id,
            interview_type=update_interview_type_data
        )

        assert interview_type is not None
        assert interview_type.id == interview_type_id
        assert interview_type.interview_type == update_interview_type_data.interview_type
        assert isinstance(interview_type, InterviewType)

    @pytest.mark.asyncio
    async def test_update_interview_type_failure(
        self,
        mock_interview_type_repo_failure,
        update_interview_type_data,
        interview_type_id=99
    ):
        with pytest.raises(IntegrityError, match="error"):
            mock_interview_type_repo_failure.update_interview_type(
                interview_type_id=interview_type_id,
                interview_type=update_interview_type_data
            )

    @pytest.mark.asyncio
    async def test_delete_interview_type_success(
        self,
        mock_interview_type_repo_success,
        interview_type_id=1
    ):
        interview_type = await mock_interview_type_repo_success.delete_interview_type(
            interview_type_id=interview_type_id
        )

        assert interview_type is True

    @pytest.mark.asyncio
    async def test_delete_interview_type_failure(
        self,
        mock_interview_type_repo_failure,
        interview_type_id=99
    ):
        with pytest.raises(NotFoundError, match="error"):
            mock_interview_type_repo_failure.delete_interview_type(
                interview_type_id=interview_type_id
            )
