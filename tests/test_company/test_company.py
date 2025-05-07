import pytest

from domain.entities.company import Company
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError


class TestCompany:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    @pytest.mark.asyncio
    async def test_create_company(self, create_company_data, mock_company_repo_interface_success):
        new_company = await mock_company_repo_interface_success.create_company(company=create_company_data)

        assert new_company is not None
        assert new_company.name == create_company_data.name
        assert new_company.link == create_company_data.link
        assert isinstance(new_company, Company)

    @pytest.mark.asyncio
    async def test_create_company_failure(self, create_company_data, mock_company_repo_interface_failure):
        with pytest.raises(IntegrityError, match="Integrity error: duplicate entry or constraint violation."):
            mock_company_repo_interface_failure.create_company(company=create_company_data)

    @pytest.mark.asyncio
    async def test_get_company_by_id(self, mock_company_repo_interface_success, company_id=0):
        query_company = await mock_company_repo_interface_success.get_company_by_id(company_id=company_id)

        assert query_company.id == company_id

    @pytest.mark.asyncio
    async def test_get_company_by_id_failure(self, mock_company_repo_interface_failure, company_id=99):
        with pytest.raises(NotFoundError, match="Not found with the given parameter"):
            mock_company_repo_interface_failure.get_company_by_id(company_id=company_id)

    @pytest.mark.asyncio
    async def test_get_all_companies(self, mock_company_repo_interface_success):
        query_companies = await mock_company_repo_interface_success.get_all_companies()

        assert len(query_companies) != 0

    @pytest.mark.asyncio
    async def test_get_all_companies_failure(self, mock_company_repo_interface_failure):
        with pytest.raises(NotFoundError, match="There's no data to show"):
            mock_company_repo_interface_failure.get_all_companies()
