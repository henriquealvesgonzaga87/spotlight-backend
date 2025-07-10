import pytest

from unittest.mock import Mock
from fastapi.testclient import TestClient

from interface_adapters.api.auth_routes import router
from containers.container import Container


client = TestClient(router)


class TestAuthRoutes:
    @pytest.fixture(autouse=True)
    def setup(self, mock_auth_use_cases_for_routes, mock_auth_use_cases):
        container = Container()
        container.wire(modules=["interface_adapters.api.auth_routes"])
        container.auth_repository.override(mock_auth_use_cases_for_routes)
        container.auth_use_cases.override(mock_auth_use_cases)
    
    def test_login_success(
        self,
        mock_auth_use_cases,
        login_data,
        token_response, 
        token_json_response
    ):
        mock_auth_use_cases.login = Mock(return_value=token_response)

        login_data_dict = login_data.model_dump()

        response = client.post("/login", json=login_data_dict)

        assert response.status_code == 200
        assert response.json() == token_json_response

    def test_login_failure(
        self,
        login_data,
    ):
        login_data_dict = login_data.model_dump()

        response = client.post("/logi", json=login_data_dict)

        assert response.status_code == 404

    def test_refresh_token_success(
        self,
        mock_auth_use_cases,
        refresh_token_header,
        token_response,
        access_token_header,
        token_json_response
    ):
        mock_auth_use_cases.refresh_token = Mock(return_value=token_response)

        headers = {**access_token_header, **refresh_token_header}

        response = client.post(
            "/refresh-token", 
            headers=headers,
        )

        assert response.status_code == 200
        assert response.json() == token_json_response

    def test_refresh_token_failure(
        self,
        refresh_token_header,
        access_token_header,
    ):
        headers = {**access_token_header, **refresh_token_header}

        response = client.post(
            "/refresh-toke", 
            headers=headers,
        )

        assert response.status_code == 404

    def test_logout_success(
        self,
        mock_auth_use_cases,
        refresh_token_header,
        refresh_token,
        access_token_header,
    ):
        mock_auth_use_cases.revoke_refresh_token = Mock(return_value=refresh_token)

        headers = {**access_token_header, **refresh_token_header}

        response = client.post("/logout", headers=headers)

        assert response.status_code == 200
        assert response.json() == {'message': 'Logout successful'}

    def test_logout_failure(
        self,
        refresh_token_header,
        access_token_header,
    ):
        headers = {**access_token_header, **refresh_token_header}

        response = client.post("/logou", headers=headers)

        assert response.status_code == 404
