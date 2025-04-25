from abc import ABC, abstractmethod
from domain.entities.company import Company


class CompanyRepositoryInterface(ABC):
    @abstractmethod
    async def create_company(self, company: Company):
        pass
