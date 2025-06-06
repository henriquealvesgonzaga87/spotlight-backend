import pytest

from unittest.mock import Mock
from fastapi.testclient import TestClient

from interface_adapters.api.job_routes import router
from containers.container import Container


client = TestClient(router)


class TestJobRoutes:
    @pytest.fixture(autouse=True)
    def setup(self, mock_job_use_cases, mock_job_for_route_tests):
        container = Container()
        container.wire(modules=["interface_adapters.api.job_routes"])
        container.job_repository.override(mock_job_for_route_tests)
        container.job_use_cases.override(mock_job_use_cases)

    @pytest.mark.asyncio
    async def test_create_job_route_success(
        self,
        mock_job_use_cases,
        create_job_data,
        job_created,
        job_json_create
    ):
        mock_job_use_cases.create_job = Mock(return_value=job_created)

        create_job_data.application_date = str(create_job_data.application_date)

        job_data = create_job_data.model_dump()

        response = client.post("/job", json=job_data)

        assert response.status_code == 201
        assert response.json() == job_json_create

    @pytest.mark.asyncio
    async def test_create_job_route_failure(
        self,
        mock_job_use_cases,
        create_job_data,
        job_created,
    ):
        mock_job_use_cases.create_job = Mock(return_value=job_created)

        create_job_data.application_date = str(create_job_data.application_date)

        job_data = create_job_data.model_dump()

        response = client.post("/jop", json=job_data)

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_all_jobs_route_success(
        self,
        mock_job_use_cases,
        jobs,
        jobs_json_response
    ):
        mock_job_use_cases.get_all_jobs = Mock(return_value=jobs)

        response = client.get("/job")

        assert response.status_code == 200
        assert response.json() == jobs_json_response

    @pytest.mark.asyncio
    async def test_get_all_jobs_route_failure(self):
        response = client.get("/jop")

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_job_by_id_route_success(
        self,
        mock_job_use_cases,
        job_created,
        job_json_create,
        job_id=1
    ):
        mock_job_use_cases.get_job_by_id = Mock(return_value=job_created)

        response = client.get(f"/job/{job_id}")

        assert response.status_code == 200
        assert response.json() == job_json_create
        assert response.json()["id"] == job_id

    @pytest.mark.asyncio
    async def test_get_job_by_id_route_failure(
        self,
        job_id=1
    ):
        response = client.get(f"/jop/{job_id}")

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_job_route_success(
        self,
        mock_job_use_cases,
        update_job_data,
        job_updated,
        job_json_update,
        job_id=1
    ):
        mock_job_use_cases.update_job = Mock(return_value=job_updated)

        update_job_data.application_date = str(update_job_data.application_date)

        job_data = update_job_data.model_dump()

        response = client.patch(f"/job/{job_id}", json=job_data)

        assert response.status_code == 200
        assert response.json() == job_json_update
        assert response.json()["id"] == job_id

    @pytest.mark.asyncio
    async def test_update_job_route_failure(
        self,
        update_job_data,
        job_id=1
    ):
        update_job_data.application_date = str(update_job_data.application_date)

        job_data = update_job_data.model_dump()

        response = client.patch(f"/jop/{job_id}", json=job_data)

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_job_route_success(
        self,
        job_id=1
    ):
        response = client.delete(f"/job/{job_id}")

        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_delete_job_route_failure(
        self,
        job_id=1
    ):
        response = client.delete(f"/jop/{job_id}")

        assert response.status_code == 404
