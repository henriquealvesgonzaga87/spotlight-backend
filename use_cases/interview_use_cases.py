from domain.entities.interview import Interview
from domain.exceptions.bad_request_error import BadRequestError
from domain.interfaces.interview_repository_interface import InterviewRepositoryInterface


class InterviewUseCases:
    def __init__(self, interview_repository: InterviewRepositoryInterface):
        self.interview_repository = interview_repository

    def _validate_id(self, id: int):
        if id < 0:
            raise BadRequestError("ID must be a positive Integer")
        
        if not isinstance(id, int):
            raise BadRequestError("ID must be an Integer")

    def create_interview(self, interview: Interview, user_id: int):
        self._validate_id(id=user_id)
        return self.interview_repository.create_interview(interview=interview, user_id=user_id)
    
    def get_all_interview(self, user_id: int):
        self._validate_id(id=user_id)
        return self.interview_repository.get_all_interview(user_id=user_id)
    
    def get_interview_by_id(self, interview_id: int):
        self._validate_id(id=interview_id)
        return self.interview_repository.get_interview_by_id(interview_id=interview_id)
    
    def update_interview(self, interview_id: int, interview: dict):
        self._validate_id(id=interview_id)
        return self.interview_repository.update_interview(
            interview_id=interview_id,
            interview=interview
        )
    
    def delete_interview(self, interview_id: int):
        self._validate_id(id=interview_id)
        return self.interview_repository.delete_interview(interview_id=interview_id)
