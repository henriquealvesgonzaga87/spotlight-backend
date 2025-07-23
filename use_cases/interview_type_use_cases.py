import re
from domain.entities.interview_type import InterviewType
from domain.exceptions.bad_request_error import BadRequestError
from domain.interfaces.interview_type_repository_interface import InterviewTypeRepositoryInterface


class InterviewTypeUseCases:
    def __init__(self, interview_type_repository: InterviewTypeRepositoryInterface):
        self.interview_type_repository = interview_type_repository

    def _validate_interview_type_data(self, string):
        regex_string = r"^[A-Z][a-zA-ZÀ-ÿ]{2,}(?:\s[a-zA-ZÀ-ÿ]{3,})*$"

        if re.match(regex_string, string) is None:
            raise BadRequestError('interview type must have at least 2 characters and start with a capital letter')
        
    def _validate_id(self, id: int):
        if id < 0:
            raise BadRequestError("ID must be a positive Integer")
        
        if not isinstance(id, int):
            raise BadRequestError("ID must be an Integer")

    def create_interview_type(self, interview_type: InterviewType):
        self._validate_interview_type_data(string=interview_type.interview_type)
        return self.interview_type_repository.create_interview_type(
            interview_type=interview_type
        )
    
    def get_all_interview_type(self, user_id: int):
        self._validate_id(id=user_id)
        return self.interview_type_repository.get_all_interview_type(user_id=user_id)
    
    def get_interview_type_by_id(self, interview_type_id: int):
        self._validate_id(id=interview_type_id)
        return self.interview_type_repository.get_interview_type_by_id(interview_type_id=interview_type_id)
    
    def update_interview_type(self, interview_type_id: int, interview_type: InterviewType):
        self._validate_id(id=interview_type_id)
        self._validate_interview_type_data(string=interview_type.interview_type)
        return self.interview_type_repository.update_interview_type(
            interview_type_id=interview_type_id,
            interview_type=interview_type
        )
    
    def delete_interview_type(self, interview_type_id: int):
        self._validate_id(id=interview_type_id)
        return self.interview_type_repository.delete_interview_type(interview_type_id=interview_type_id)
