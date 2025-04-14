from unittest.mock import AsyncMock, Mock
import pytest
from fastapi.testclient import TestClient
from containers.container import Container

from domain.exceptions.integrity_error import IntegrityError
from interface_adapters.api.user_routes import router


client = TestClient(router)


class TestUserRoutes:
    @pytest.fixture(autouse=True)
    def setup(self, mock_user_repo_failure, mock_user_repository_for_route_tests):
        container = Container()
        container.wire(modules=["interface_adapters.api.user_routes"])
        container.user_repository.override(mock_user_repository_for_route_tests)
        container.user_use_cases.override(mock_user_repo_failure)
        
    @pytest.mark.asyncio
    async def test_route_create_user_success(self, user_created, create_user_data, mock_user_repo_failure):
        # Simula o comportamento do caso de uso para o teste
        mock_user_repo_failure.create_user = Mock(return_value=user_created)

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

            client.post("/user", json=user_data)

            mock_user_repo_failure.create_user(user=user_data)
