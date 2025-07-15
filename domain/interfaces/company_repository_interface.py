from abc import ABC, abstractmethod
from domain.entities.company import Company


class CompanyRepositoryInterface(ABC):
    @abstractmethod
    async def create_company(self, company: Company):
        pass

    @abstractmethod
    async def get_company_by_id(self, company_id: int):
        pass

    @abstractmethod
    async def get_all_companies(self):
        pass

    @abstractmethod
    async def update_company(self, company_id: int, company: Company, user_id: int):
        pass

    @abstractmethod
    async def delete_company(self, company_id: int):
        pass
