from sqlalchemy.orm import Session

from domain.entities.company import Company
from domain.interfaces.company_repository_interface import CompanyRepositoryInterface


class SQLAlchemyCompanyRepository(CompanyRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session
    
    def create_company(self, company: Company) -> Company:
        pass
    