from domain.exceptions.bad_request_error import BadRequestError
from domain.interfaces.company_repository_interface import CompanyRepositoryInterface
from domain.entities.company import Company


class CompanyUseCases:
    def __init__(self, company_repository: CompanyRepositoryInterface):
        self.company_repository = company_repository

    def _validate_company_id(self, company_id):
        if type(company_id) != int:
            raise BadRequestError("The given ID must be an integer")
        
        if company_id is None:
            raise BadRequestError("ID cannot be empty")

    def create_company(self, company: Company):
        return self.company_repository.create_company(company=company)
    
    def get_company_by_id(self, company_id: int):
        self._validate_company_id(company_id=company_id)

        return self.company_repository.get_company_by_id(company_id=company_id)
    
    def get_all_companies(self):
        return self.company_repository.get_all_companies()
