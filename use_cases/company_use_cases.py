from domain.interfaces.company_repository_interface import CompanyRepositoryInterface
from domain.entities.company import Company


class CompanyUseCases:
    def __init__(self, company_repository: CompanyRepositoryInterface):
        self.company_repository = company_repository

    def create_user(self, company: Company):
        return self.company_repository.create_company(company=company)
    
