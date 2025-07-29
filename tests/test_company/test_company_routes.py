from unittest.mock import Mock
import pytest
from fastapi.testclient import TestClient
from containers.container import Container

from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError
from interface_adapters.api.company_routes import router


client = TestClient(router)


class TestCompanyRoutes:
    @pytest.fixture(autouse=True)
    def setup(self, mock_company_use_cases, mock_company_repository_for_route_tests):
        container = Container()
        container.wire(modules=["interface_adapters.api.company_routes"])
        container.company_repository.override(mock_company_repository_for_route_tests)
        container.company_use_cases.override(mock_company_use_cases)
        
    @pytest.mark.asyncio
    async def test_route_create_company_success(
        self, 
        company_created, 
        create_company_data, 
        mock_company_use_cases,
        headers,
    ):
        
        mock_company_use_cases.create_company = Mock(return_value=company_created)

        create_company_data.link = str(create_company_data.link)
        company_data = create_company_data.model_dump()

        response = client.post("/company", headers=headers, json=company_data)

        assert response.status_code == 201
        assert response.json() == {
            "id": 0,
            "name": "Test",
            "link": "https://www.test.com/",
            "created_at": "2025-04-24T20:29:20.461333",
            "updated_at": None,
        }

    @pytest.mark.asyncio
    async def test_route_create_company_failure(self, mock_company_repo_interface_failure, create_company_data):
        with pytest.raises(IntegrityError, match="Integrity error: duplicate entry or constraint violation."):
            company_data = create_company_data.model_dump()

            mock_company_repo_interface_failure.create_company(company=company_data)

            client.post("/company", json=company_data)

    @pytest.mark.asyncio
    async def test_route_get_company_by_id_success(
        self, 
        mock_company_use_cases, 
        company_created,
        headers,
        company_id=0
    ):
        
        mock_company_use_cases.get_company_by_id = Mock(return_value=company_created)

        response = client.get(f'/company/{company_id}', headers=headers)

        assert response.status_code == 200
        assert response.json() == {
            "id": 0,
            "name": "Test",
            "link": "https://www.test.com/",
            "created_at": "2025-04-24T20:29:20.461333",
            "updated_at": None,
        }

    @pytest.mark.asyncio
    async def test_route_get_company_by_id_failure(self, mock_company_repo_interface_failure, company_id=99):
        with pytest.raises(NotFoundError, match="Not found with the given parameter"):
            mock_company_repo_interface_failure.get_company_by_id(company_id=company_id)
            client.get(f"company/{company_id}")

    @pytest.mark.asyncio
    async def test_route_get_all_companies_success(
        self, 
        mock_company_use_cases, 
        companies,
        headers,
    ):
        
        mock_company_use_cases.get_all_companies = Mock(return_value=companies)

        response = client.get("/company", headers=headers)

        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert response.json() == [
            {
                'id': 0, 
                'name': 'Test', 
                'link': 'https://www.test.com/', 
                'created_at': '2025-04-24T20:29:20.461333', 
                'updated_at': None
            }, 
            {
                'id': 1, 
                'name': 'Test One', 
                'link': 'https://www.test.com/', 
                'created_at': '2025-04-24T20:29:20.461333', 
                'updated_at': None
            }, 
            {
                'id': 2, 
                'name': 'Test Two', 
                'link': 'https://www.test.com/', 
                'created_at': '2025-04-24T20:29:20.461333', 
                'updated_at': None
            }
        ]

    @pytest.mark.asyncio
    async def test_route_get_all_companies_failure(self, mock_company_repo_interface_failure):
        with pytest.raises(NotFoundError, match="There's no data to show"):
            mock_company_repo_interface_failure.get_all_companies()
            client.get("/company")

    @pytest.mark.asyncio
    async def test_route_update_company_success(
        self, 
        mock_company_use_cases, 
        company_updated, 
        update_company_data,
        headers,
        company_id=0
    ):
        mock_company_use_cases.update_company = Mock(return_value=company_updated)

        update_company_data.link = str(update_company_data.link)
        company_data = update_company_data.model_dump()

        response = client.patch(f"/company/{company_id}", headers=headers, json=company_data)

        assert response.status_code == 200
        assert response.json() == {
            'id': 0, 
            'name': 'Test Updated', 
            'link': 'https://www.testupdated.com/', 
            'created_at': '2025-04-24T20:29:20.461333', 
            'updated_at': '2025-04-24T20:29:20.461333'
        }

    @pytest.mark.asyncio
    async def test_route_update_company_failure(self, mock_company_repo_interface_failure, update_company_data, company_id=99):
        with pytest.raises(IntegrityError, match="Integrity error: duplicate entry or constraint violation."):
            mock_company_repo_interface_failure.update_company(company_id=company_id, company=update_company_data)
            client.patch(f"/company/{company_id}", json=update_company_data)

    @pytest.mark.asyncio
    async def test_route_delete_company_success(
        self, 
        mock_company_use_cases, 
        company_created,
        headers,
        company_id=0
    ):
        mock_company_use_cases.delete_company = Mock(return_value=company_created)
        
        mock_company_use_cases.delete_company(company_id=company_id)

        response = client.delete(f"/company/{company_id}", headers=headers)

        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_route_delete_company_failure_id_not_found(self, mock_company_repo_interface_failure, company_id=99):
        with pytest.raises(NotFoundError, match="Not found with the given parameter"):
            mock_company_repo_interface_failure.delete_company(company_id=company_id)
            client.delete(f"/company/{company_id}")

    @pytest.mark.asyncio
    async def test_route_delete_company_failure_for_exception(self, mock_company_repo_interface_failure, company_id=99):
        mock_company_repo_interface_failure.delete_company = Mock(side_effect=IntegrityError("An error occurred while deleting the company."))

        with pytest.raises(IntegrityError, match="An error occurred while deleting the company."):
            mock_company_repo_interface_failure.delete_company(company_id=company_id)
            client.delete(f"/company/{company_id}")
