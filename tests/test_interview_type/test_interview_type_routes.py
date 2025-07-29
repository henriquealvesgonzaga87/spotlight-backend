import pytest
from unittest.mock import Mock
from fastapi.testclient import TestClient

from containers.container import Container
from interface_adapters.api.interview_type_routes import router


client = TestClient(router)


class TestInterviewTypeRoutes:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        mock_interview_type_use_cases,
        mock_interview_type_repo_for_route_tests
    ):
        container = Container()
        container.wire(modules=["interface_adapters.api.interview_type_routes"])
        container.interview_type_repository.override(mock_interview_type_repo_for_route_tests)
        container.interview_type_use_cases.override(mock_interview_type_use_cases)

    @pytest.mark.asyncio
    async def test_create_interview_type_route_success(
        self,
        mock_interview_type_use_cases,
        create_interview_type_data,
        interview_type_created,
        interview_type_create_json_response,
        headers,
    ):
        mock_interview_type_use_cases.create_interview_type = Mock(return_value=interview_type_created)

        interview_type_data = create_interview_type_data.model_dump()

        response = client.post("/interview_type", headers=headers, json=interview_type_data)

        assert response.status_code == 201
        assert response.json() == interview_type_create_json_response

    @pytest.mark.asyncio
    async def test_create_interview_type_route_failure(
        self,
        create_interview_type_data,
    ):
        
        response = client.post("/interview_typ", json=create_interview_type_data.model_dump())

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_all_interview_type_route_success(
        self,
        mock_interview_type_use_cases,
        interview_types,
        interview_types_json_response,
        headers,
    ):
        mock_interview_type_use_cases.get_all_interview_type = Mock(return_value=interview_types)

        response = client.get("/interview_type", headers=headers)

        assert response.status_code == 200
        assert response.json() == interview_types_json_response

    @pytest.mark.asyncio
    async def test_get_all_interview_type_route_failure(
        self,
    ):
        response = client.get("/interview_typ")

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_interview_type_by_id_route_success(
        self,
        mock_interview_type_use_cases,
        interview_type_created,
        interview_type_create_json_response,
        headers,
        interview_type_id=1
    ):
        mock_interview_type_use_cases.get_interview_type_by_id = Mock(return_value=interview_type_created)

        response = client.get(f"/interview_type/{interview_type_id}", headers=headers)

        assert response.status_code == 200
        assert response.json() == interview_type_create_json_response
        assert response.json()["id"] == interview_type_id

    @pytest.mark.asyncio
    async def test_get_interview_type_by_id_route_failure(
        self,
        interview_type_id=1
    ):
        response = client.get(f"/interview_typ/{interview_type_id}")

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_interview_type_route_success(
        self,
        mock_interview_type_use_cases,
        update_interview_type_data,
        interview_type_updated,
        interview_type_update_json_response,
        headers,
        interview_type_id=1
    ):
        mock_interview_type_use_cases.update_interview_type = Mock(return_value=interview_type_updated)

        response = client.patch(f"/interview_type/{interview_type_id}", headers=headers, json=update_interview_type_data.model_dump())

        assert response.status_code == 200
        assert response.json() == interview_type_update_json_response
        assert response.json()["id"] == interview_type_id

    @pytest.mark.asyncio
    async def test_update_interview_type_route_failure(
        self,
        update_interview_type_data,
        interview_type_id=1
    ):
        response = client.patch(f"/interview_typ/{interview_type_id}", json=update_interview_type_data.model_dump())

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_interview_type_route_success(
        self,
        mock_interview_type_use_cases,
        headers,
        interview_type_id=1
    ):
        mock_interview_type_use_cases.delete_interview_type = Mock(return_value=True)

        response = client.delete(f"/interview_type/{interview_type_id}", headers=headers)

        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_delete_interview_type_route_failure(
        self,
        interview_type_id=1
    ):
        response = client.delete(f"/interview_typ/{interview_type_id}")

        assert response.status_code == 404
