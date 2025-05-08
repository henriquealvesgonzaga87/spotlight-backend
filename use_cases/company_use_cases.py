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
        
    def _convert_url_to_string(self, url):
        url_to_string = url.unicode_string()

        return url_to_string

    def create_company(self, company: Company):
        return self.company_repository.create_company(company=company)
    
    def get_company_by_id(self, company_id: int):
        self._validate_company_id(company_id=company_id)

        return self.company_repository.get_company_by_id(company_id=company_id)
    
    def get_all_companies(self):
        return self.company_repository.get_all_companies()
    
    def update_company(self, company_id: int, company: Company):
        self._validate_company_id(company_id=company_id)

        return self.company_repository.update_company(company_id=company_id, company=company)
    
    def delete_company(self, company_id: int):
        self._validate_company_id(company_id=company_id)

        return self.company_repository.delete_company(company_id=company_id)
