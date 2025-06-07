from datetime import datetime

from sqlalchemy.orm import Session

from domain.entities.interview_type import InterviewType
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError
from domain.interfaces.interview_type_repository_interface import InterviewTypeRepositoryInterface


class SQLAlchemyInterviewTypeRepository(InterviewTypeRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def create_interview_type(self, interview_type: InterviewType):
        try:
            interview_type.created_at = datetime.utcnow()

            self.session.add(interview_type)
            self.session.commit()
            self.session.refresh(interview_type)

            return interview_type

        except IntegrityError:
            self.session.rollback()
            raise IntegrityError("Integrity Error must be unique")
        
        finally:
            self.session.close()

    def get_all_interview_type(self):
        inteview_types = self.session.query(InterviewType).all()

        if len(inteview_types) == 0:
            raise NotFoundError("There are no data to show")
        
        return inteview_types
