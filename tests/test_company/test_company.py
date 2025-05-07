import pytest

from domain.entities.company import Company


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
