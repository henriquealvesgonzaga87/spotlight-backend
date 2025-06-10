import pytest

from unittest.mock import Mock
from fastapi.testclient import TestClient

from interface_adapters.api.interview_routes import router
from containers.container import Container


client = TestClient(router)


class TestInterviewRoutes:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        mock_interview_use_cases,
        mock_interview_repo_for_route_tests
    ):
        container = Container()
        container.wire(modules=["interface_adapters.api.interview_routes"])
        container.interview_repository.override(mock_interview_repo_for_route_tests)
        container.interview_use_cases.override(mock_interview_use_cases)

    @pytest.mark.asyncio
    async def test_create_interview_route_success(
        self,
        mock_interview_use_cases,
        create_interview_data,
        interview_created,
        create_interview_json_response
    ):
        mock_interview_use_cases.create_interview = Mock(return_value=interview_created)

        create_interview_data.interview_date = str(create_interview_data.interview_date)

        interview_data = create_interview_data.model_dump()

        response = client.post("/interview", json=interview_data)

        assert response.status_code == 201
        assert response.json() == create_interview_json_response

    @pytest.mark.asyncio
    async def test_create_interview_route_failure(
        self,
        create_interview_data,
    ):
        create_interview_data.interview_date = str(create_interview_data.interview_date)

        interview_data = create_interview_data.model_dump()

        response = client.post("/intervie", json=interview_data)

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_all_interview_route_success(
        self,
        interviews,
        mock_interview_use_cases,
        get_all_interviews_json_response
    ):
        mock_interview_use_cases.get_all_interview = Mock(return_value=interviews)

        response = client.get("/interview")

        assert response.status_code == 200
        assert response.json() == get_all_interviews_json_response

    @pytest.mark.asyncio
    async def test_get_all_interview_route_failure(
        self,
    ):
        response = client.get("/intervie")

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_interview_by_id_route_success(
        self,
        mock_interview_use_cases,
        interview_created,
        create_interview_json_response,
        interview_id=1
    ):
        mock_interview_use_cases.get_interview_by_id = Mock(return_value= interview_created)

        response = client.get(f"/interview/{interview_id}")

        assert response.status_code == 200
        assert response.json()["id"] == interview_id
        assert response.json() == create_interview_json_response

    @pytest.mark.asyncio
    async def test_get_interview_by_id_route_failure(
        self,
        interview_id=1
    ):
        response = client.get(f"/intervie/{interview_id}")

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_interview_route_success(
        self,
        mock_interview_use_cases,
        interview_updated,
        update_interview_data,
        update_interview_json_response,
        interview_id=1
    ):
        mock_interview_use_cases.update_interview = Mock(return_value=interview_updated)

        update_interview_data.interview_date = str(update_interview_data.interview_date)

        interview_data = update_interview_data.model_dump()

        response = client.patch(f"/interview/{interview_id}", json=interview_data)

        assert response.status_code == 200
        assert response.json() == update_interview_json_response
        assert response.json()["id"] == interview_id
    
    @pytest.mark.asyncio
    async def test_update_interview_route_failure(
        self,
        update_interview_data,
        interview_id=99
    ):
        update_interview_data.interview_date = str(update_interview_data.interview_date)

        interview_data = update_interview_data.model_dump()

        response = client.patch(f"/intervie/{interview_id}", json=interview_data)

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_interview_route_success(
        self,
        mock_interview_use_cases,
        interview_id=1
    ):
        mock_interview_use_cases.delete_interview = Mock(return_value=True)

        response = client.delete(f"/interview/{interview_id}")

        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_delete_interview_route_failure(
        self,
        interview_id=1
    ):
        response = client.delete(f"/intervie/{interview_id}")

        assert response.status_code == 404
