from sqlalchemy.orm import Session

from domain.entities.company import Company
from domain.exceptions.integrity_error import IntegrityError
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
    