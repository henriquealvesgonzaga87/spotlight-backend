from unittest.mock import Mock
import pytest
from fastapi.testclient import TestClient
from containers.container import Container

from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError
from interface_adapters.api.user_routes import router


client = TestClient(router)


class TestUserRoutes:
    @pytest.fixture(autouse=True)
    def setup(self, mock_user_use_cases, mock_user_repository_for_route_tests):
        container = Container()
        container.wire(modules=["interface_adapters.api.user_routes"])
        container.user_repository.override(mock_user_repository_for_route_tests)
        container.user_use_cases.override(mock_user_use_cases)
        
    @pytest.mark.asyncio
    async def test_route_create_user_success(self, user_created, create_user_data, mock_user_use_cases):
        # Simula o comportamento do caso de uso para o teste
        mock_user_use_cases.create_user = Mock(return_value=user_created)

        # Dados de entrada
        user_data = create_user_data.model_dump()

        # Faz a requisição POST
        response = client.post("/user", json=user_data)

        # Verifica o status e o corpo da resposta
        assert response.status_code == 201
        assert response.json() == {
            "id": 0,
            "name":'Test',
            "email":'test@mail.com',
            "password":'test'
        }

    @pytest.mark.asyncio
    async def test_route_create_user_failure(self, mock_user_repo_failure, create_user_data):
        with pytest.raises(IntegrityError, match="Integrity error occurred"):
            user_data = create_user_data.model_dump()

            mock_user_repo_failure.create_user(user=user_data)

            client.post("/user", json=user_data)

    @pytest.mark.asyncio
    async def test_route_get_user_by_id_success(self, mock_user_use_cases, user_created, user_id=0):
        mock_user_use_cases.get_user_by_id = Mock(return_value=user_created)

        response = client.get(f'/user/{user_id}')

        assert response.status_code == 200
        assert response.json() == {
            "id": 0,
            "name":'Test',
            "email":'test@mail.com',
            "password":'test'
        }

    @pytest.mark.asyncio
    async def test_route_get_user_by_id_failure(self, mock_user_repo_failure, user_id=99):
        
        with pytest.raises(NotFoundError):
            mock_user_repo_failure.get_user_by_id(user_id=user_id)
            client.get(f'/user/{user_id}')
