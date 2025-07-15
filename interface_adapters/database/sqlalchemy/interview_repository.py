from datetime import datetime
from sqlalchemy.orm import Session

from domain.entities.interview import Interview
from domain.entities.job import Job
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError
from domain.exceptions.unauthorized_error import UnauthorizedError
from domain.interfaces.interview_repository_interface import InterviewRepositoryInterface


class SQLAlchemyInterviewRepository(InterviewRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def create_interview(self, interview: Interview, user_id: int):
        query_job_for_control_ownership = self.session.query(Job)\
            .filter(Job.user_id == user_id)\
            .filter(Job.id == interview.job_id)\
            .first()
        
        if query_job_for_control_ownership is None:
            raise UnauthorizedError("You are not allowed to do this operation")
        
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

    def get_all_interview(self, user_id: int):
        query_interview = self.session.query(Interview)\
            .join(Interview.job)\
            .filter(Job.user_id == user_id)\
            .all()

        if len(query_interview) == 0:
            raise NotFoundError("There is no data to show")
        
        return query_interview
    
    def get_interview_by_id(self, interview_id: int, user_id: int):
        query_interview = self.session.query(Interview)\
            .join(Interview.job)\
            .filter(Job.user_id == user_id)\
            .filter(Interview.id == interview_id)\
            .first()

        if query_interview is None:
            raise NotFoundError("Not found with the given parameter")
        
        return query_interview
    
    def update_interview(self, interview_id: int, interview: dict, user_id: int):
        query_interview = self.get_interview_by_id(interview_id=interview_id, user_id=user_id)

        try:
            for key, value in interview.items():
                setattr(query_interview, key, value)

            query_interview.updated_at = datetime.utcnow()

            self.session.add(query_interview)
            self.session.commit()
            self.session.refresh(query_interview)

            return query_interview
        
        except IntegrityError:
            self.session.rollback()
            raise IntegrityError("Something went wrong while updating")
        
        finally:
            self.session.close()

    def delete_interview(self, interview_id: int, user_id: int):
        query_interview = self.get_interview_by_id(interview_id=interview_id, user_id=user_id)

        try:
            self.session.delete(query_interview)
            self.session.commit()

            return query_interview
        
        except IntegrityError:
            self.session.rollback()
            raise IntegrityError("Impossible to delete")
        
        finally:
            self.session.close()
