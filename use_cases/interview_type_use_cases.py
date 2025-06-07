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

    def create_interview_type(self, interview_type: InterviewType):
        self._validate_interview_type_data(string=interview_type.interview_type)
        return self.interview_type_repository.create_interview_type(
            interview_type=interview_type
        )
