from datetime import datetime

from sqlalchemy.orm import Session

from domain.entities.interview import Interview
from domain.entities.interview_type import InterviewType
from domain.entities.job import Job
from domain.exceptions.argument_error import ArgumentError
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

    def get_all_interview_type(self, user_id: int):
        try:
            inteview_types = self.session.query(InterviewType)\
                .join(InterviewType.interview)\
                .join(Interview.job)\
                .filter(Job.user_id == user_id)\
                .all()

            if len(inteview_types) == 0:
                raise NotFoundError("There are no data to show")
            
            return inteview_types
        
        except IntegrityError as e:
            raise IntegrityError(f"Something went wrong to get the data: {e}")
        
        except ArgumentError as e:
            raise ArgumentError(f"!!!ERROR!!!: {e}")
        
        finally:
            self.session.close()
    
    def get_interview_type_by_id(self, interview_type_id: int, user_id: int):
        try:
            interview_type = self.session.query(InterviewType)\
                .filter(InterviewType.id == interview_type_id)\
                .join(InterviewType.interview)\
                .join(Interview.job)\
                .filter(Job.user_id == user_id)\
                .first()

            if interview_type is None:
                raise NotFoundError("Not found with the given parameter")

            return interview_type
        
        except IntegrityError as e:
            raise IntegrityError(f"Something went wrong to get the data: {e}")
        
        except ArgumentError as e:
            raise ArgumentError(f"!!!ERROR!!!: {e}")
        
        finally:
            self.session.close()
    
    def update_interview_type(self, interview_type_id: int, interview_type: InterviewType, user_id: int):
        query_interview_type = self.get_interview_type_by_id(
            interview_type_id=interview_type_id,
            user_id=user_id
        )

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

    def delete_interview_type(self, interview_type_id: int, user_id: int):
        try:
            query_interview_type = self.get_interview_type_by_id(
                interview_type_id=interview_type_id,
                user_id=user_id
            )

            self.session.delete(query_interview_type)
            self.session.commit()

            return query_interview_type
        
        except IntegrityError:
            self.session.rollback()
            raise IntegrityError("Something went wrong while saving")
        
        finally:
            self.session.close()
