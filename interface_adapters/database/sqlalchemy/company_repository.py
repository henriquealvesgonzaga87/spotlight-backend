from sqlalchemy import desc
from sqlalchemy.orm import Session

from domain.entities.company import Company
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError
from domain.interfaces.company_repository_interface import CompanyRepositoryInterface
from datetime import datetime


class SQLAlchemyCompanyRepository(CompanyRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session
    
    def create_company(self, company: Company) -> Company:
        try:
            company.created_at = datetime.utcnow()
            self.session.add(company)
            self.session.commit()
            self.session.refresh(company)
            return company
        except Exception as e:
            self.session.rollback()
            raise IntegrityError(message=f"Integrity error: duplicate entry or constraint violation. ERROR: {e}")
        finally:
            self.session.close()

    def get_company_by_id(self, company_id: int) -> Company:
        company = self.session.query(Company).filter(Company.id == company_id).first()

        if company is None:
            raise NotFoundError(message='Not found with the given parameter')
        
        return company
    
    def get_all_companies(self):
        companies = self.session.query(Company).all()

        if len(companies) == 0:
            raise NotFoundError(message="There's no data to show")

        return companies
    