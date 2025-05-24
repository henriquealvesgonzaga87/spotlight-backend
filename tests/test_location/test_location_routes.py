import pytest

from unittest.mock import Mock
from fastapi.testclient import TestClient

from interface_adapters.api.location_routes import router
from containers.container import Container


client = TestClient(router)


class TestLocationRoutes:
    @pytest.fixture(autouse=True)
    def setup(self, mock_location_use_cases, mock_location_repository_for_route_tests):
        container = Container()
        container.wire(modules=["interface_adapters.api.location_routes"])
        container.location_repository.override(mock_location_repository_for_route_tests)
        container.location_use_cases.override(mock_location_use_cases)

    @pytest.mark.asyncio
    async def test_create_country_route_success(self):
        response = client.post("/location/country")

        assert response.status_code == 201
        assert response.json() == "Countries created successfully"

    @pytest.mark.asyncio
    async def test_create_country_route_failure(self):
        response = client.post("/location/countr")

        assert response.status_code == 404
        assert response.content.decode("utf-8") == "Not Found"
