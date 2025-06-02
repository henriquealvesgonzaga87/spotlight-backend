import pytest

from unittest.mock import Mock
from fastapi.testclient import TestClient

from interface_adapters.api.application_stage_routes import router
from containers.container import Container


client = TestClient(router)


class TestApplicationStageRoutes:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        mock_application_stage_use_cases,
        mock_application_stage_for_route_tests
    ):
        container = Container()
        container.wire(modules=["interface_adapters.api.application_stage_routes"])
        container.application_stage_repository.override(mock_application_stage_for_route_tests)
        container.application_stage_use_cases.override(mock_application_stage_use_cases)

    @pytest.mark.asyncio
    async def test_create_application_stage_route_success(
        self,
        mock_application_stage_use_cases,
        create_application_stage_data,
        application_stage_created,
        application_stage_json
    ):
        mock_application_stage_use_cases.create_application_stage = Mock(return_value=application_stage_created)

        application_stage_data = create_application_stage_data.model_dump()

        response = client.post("/application_stage", json=application_stage_data)

        assert response.status_code == 201
        assert response.json() == application_stage_json

    @pytest.mark.asyncio
    async def test_create_application_stage_route_failure(
        self,
        create_application_stage_data,
    ):
        application_stage_data = create_application_stage_data.model_dump()

        response = client.post("/application_stag", json=application_stage_data)

        assert response.status_code == 404


    @pytest.mark.asyncio
    async def test_get_all_application_stage_route_success(
        self,
        mock_application_stage_use_cases,
        applications_stage,
        applications_stage_json
    ):
        mock_application_stage_use_cases.get_all_application_stage = Mock(return_value=applications_stage)

        response = client.get("/application_stage")

        assert response.status_code == 200
        assert response.json() == applications_stage_json

    @pytest.mark.asyncio
    async def test_get_all_application_stage_route_failure(
        self,
    ):
        response = client.get("/application_stag")

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_application_stage_by_id_route_success(
        self,
        mock_application_stage_use_cases,
        application_stage_created,
        application_stage_json,
        application_stage_id=1,
    ):
        mock_application_stage_use_cases.get_application_stage_by_id = Mock(return_value=application_stage_created)

        response = client.get(f"/application_stage/{application_stage_id}")

        assert response.status_code == 200
        assert response.json() == application_stage_json
        assert response.json()["id"] == application_stage_id

    @pytest.mark.asyncio
    async def test_get_application_stage_by_id_route_failure(
        self,
        application_stage_id=99,
    ):
        response = client.get(f"/application_stag/{application_stage_id}")

        assert response.status_code == 404
