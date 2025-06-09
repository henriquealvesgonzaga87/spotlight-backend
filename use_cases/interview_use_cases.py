from domain.entities.interview import Interview
from domain.interfaces.interview_repository_interface import InterviewRepositoryInterface


class InterviewUseCases:
    def __init__(self, interview_repository: InterviewRepositoryInterface):
        self.interview_repository = interview_repository

    def create_interview(self, interview: Interview):
        return self.interview_repository.create_interview(interview=interview)
