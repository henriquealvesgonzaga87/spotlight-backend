import pytest
import json

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

    @pytest.mark.asyncio
    async def test_get_countries_success(self, mock_location_use_cases, countries):
        mock_location_use_cases.get_countries = Mock(return_value=countries)

        response = client.get("/location/country")

        assert response.status_code == 200
        assert response.json() == [
            {'id': 0, 'common_name': 'Andorra', 'code': 'AD'}, 
            {'id': 1, 'common_name': 'United Arab Emirates', 'code': 'AE'}, 
            {'id': 2, 'common_name': 'Afghanistan', 'code': 'AF'}
        ]

    @pytest.mark.asyncio
    async def test_get_countries_failure(self):
        response = client.get("location/countr")

        assert response.status_code == 404
        assert response.content.decode("utf-8") == "Not Found"

    @pytest.mark.asyncio
    async def test_get_country_by_id_success(self, mock_location_use_cases, country, country_id=0):
        mock_location_use_cases.get_country_by_id = Mock(return_value=country)

        response = client.get(f"/location/country/{country_id}")

        assert response.status_code == 200
        assert response.json() == {'id': 0, 'common_name': 'Andorra', 'code': 'AD'}

    @pytest.mark.asyncio
    async def test_get_country_by_id_failure(self, country_id=300):
        response = client.get(f"/location/countr/{country_id}")

        assert response.status_code == 404
        assert response.content.decode("utf-8") == "Not Found"

    @pytest.mark.asyncio
    async def test_get_states_success(self, mock_location_use_cases, states):
        mock_location_use_cases.get_states = Mock(return_value=states)

        response = client.get("/location/country/state/Andorra")

        assert response.status_code == 200
        assert response.json() == [
            {'id': 0, 'name': 'Escaldes-Engordany', 'code': '08', 'admin_code': 8, 'country_id': 1}, 
            {'id': 1, 'name': 'Sant Julià de Loria', 'code': '06', 'admin_code': 6, 'country_id': 1}, 
            {'id': 2, 'name': 'Ordino', 'code': '05', 'admin_code': 5, 'country_id': 1}
        ]

    @pytest.mark.asyncio
    async def test_get_states_failure(self):
        response = client.get("/location/stat/Andorra")

        assert response.status_code == 404
        assert response.content.decode() == "Not Found"

    @pytest.mark.asyncio
    async def test_get_state_by_id_success(self, mock_location_use_cases, state, state_id=0):
        mock_location_use_cases.get_state_by_id = Mock(return_value=state)

        response = client.get(f"/location/state/{state_id}")

        assert response.status_code == 200
        assert response.json() == {'id': 0, 'name': 'Escaldes-Engordany', 'code': '08', 'admin_code': 8, 'country_id': 1}
        assert response.json()["id"] == state_id

    @pytest.mark.asyncio
    async def test_get_state_by_id_failure(self):
        response = client.get("/location/stat/99")

        assert response.status_code == 404
        assert response.content.decode() == "Not Found"
