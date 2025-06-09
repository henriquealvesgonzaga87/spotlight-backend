from datetime import datetime
from sqlalchemy.orm import Session

from domain.entities.interview import Interview
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError
from domain.interfaces.interview_repository_interface import InterviewRepositoryInterface


class SQLAlchemyInterviewRepository(InterviewRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def create_interview(self, interview: Interview):
        try:
            interview.created_at = datetime.utcnow()

            self.session.add(interview)
            self.session.commit()
            self.session.refresh(interview)

            return interview
        
        except IntegrityError:
            self.session.rollback()
            raise IntegrityError("Error on saving the interview")
        
        finally:
            self.session.close()

    def get_all_interview(self):
        query_interview = self.session.query(Interview).all()

        if len(query_interview) == 0:
            raise NotFoundError("There is no data to show")
        
        return query_interview
