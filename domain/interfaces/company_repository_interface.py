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
