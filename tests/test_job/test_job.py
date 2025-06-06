import pytest

from domain.entities.job import Job
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError


class TestJob:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    @pytest.mark.asyncio
    async def test_create_job_success(
        self,
        mock_job_repo_success,
        create_job_data
    ):
        new_job = await mock_job_repo_success.create_job(job=create_job_data)

        assert new_job is not None
        assert isinstance(new_job, Job)

    @pytest.mark.asyncio
    async def test_create_job_failure(
        self,
        mock_job_repo_failure,
        create_job_data
    ):
        with pytest.raises(IntegrityError, match="error"):
            mock_job_repo_failure.create_job(job=create_job_data)

    @pytest.mark.asyncio
    async def test_get_all_jobs_success(
        self,
        mock_job_repo_success,
    ):
        jobs = await mock_job_repo_success.get_all_jobs()

        assert len(jobs) > 0
        assert isinstance(jobs[0], Job)
        assert isinstance(jobs[1], Job)
        assert isinstance(jobs[2], Job)

    @pytest.mark.asyncio
    async def test_get_all_jobs_failure(
        self,
        mock_job_repo_failure
    ):
        with pytest.raises(NotFoundError, match="error"):
            mock_job_repo_failure.get_all_jobs()

    @pytest.mark.asyncio
    async def test_get_job_by_id_success(
        self,
        mock_job_repo_success,
        job_id=1
    ):
        job = await mock_job_repo_success.get_job_by_id(job_id=job_id)

        assert job is not None
        assert job.id == job_id
        assert isinstance(job, Job)

    @pytest.mark.asyncio
    async def test_get_job_by_id_failure(
        self,
        mock_job_repo_failure,
        job_id=99
    ):
        with pytest.raises(NotFoundError, match="error"):
            mock_job_repo_failure.get_job_by_id(job_id=job_id)

    @pytest.mark.asyncio
    async def test_update_job_success(
        self,
        mock_job_repo_success,
        update_job_data,
        job_id=1
    ):
        job = await mock_job_repo_success.update_job(
            job_id=job_id,
            job=update_job_data
        )

        assert job is not None
        assert job.id == job_id
        assert isinstance(job, Job)

    @pytest.mark.asyncio
    async def test_update_job_failure(
        self,
        mock_job_repo_failure,
        update_job_data,
        job_id=1
    ):
        with pytest.raises(IntegrityError, match="error"):
            mock_job_repo_failure.update_job(
                job_id=job_id,
                job=update_job_data
            )

    @pytest.mark.asyncio
    async def test_delete_job_success(
        self,
        mock_job_repo_success,
        job_id=1
    ):
        job = await mock_job_repo_success.delete_job(job_id=job_id)

        assert job is True

    @pytest.mark.asyncio
    async def test_delete_job_failure(
        self,
        mock_job_repo_failure,
        job_id=99
    ):
        with pytest.raises(NotFoundError, match="error"):
            mock_job_repo_failure.delete_job(job_id=job_id)
