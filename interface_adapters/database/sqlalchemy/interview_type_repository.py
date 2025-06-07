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
    
    def get_interview_type_by_id(self, interview_type_id: int):
        interview_type = self.session.query(InterviewType).filter(InterviewType.id == interview_type_id).first()

        if interview_type is None:
            raise NotFoundError("Not found with the given parameter")

        return interview_type
    
    def update_interview_type(self, interview_type_id: int, interview_type: InterviewType):
        query_interview_type = self.get_interview_type_by_id(interview_type_id=interview_type_id)

        try:
            query_interview_type.interview_type = interview_type.interview_type
            query_interview_type.updated_at = datetime.utcnow()

            self.session.add(query_interview_type)
            self.session.commit()
            self.session.refresh(query_interview_type)

            return query_interview_type
        
        except IntegrityError:
            self.session.rollback()
            raise IntegrityError("Something went wrong while saving")
        
        finally:
            self.session.close()
