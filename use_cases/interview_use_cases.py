from domain.entities.interview import Interview
from domain.interfaces.interview_repository_interface import InterviewRepositoryInterface
from utils.utils import verify_id


class InterviewUseCases:
    def __init__(self, interview_repository: InterviewRepositoryInterface):
        self.interview_repository = interview_repository

    def create_interview(self, interview: Interview, user_id: int):
        verify_id(id_value=user_id)
        return self.interview_repository.create_interview(interview=interview, user_id=user_id)
    
    def get_all_interview(self, user_id: int):
        verify_id(id_value=user_id)
        return self.interview_repository.get_all_interview(user_id=user_id)
    
    def get_interview_by_id(self, interview_id: int, user_id: int):
        verify_id(id_value=[interview_id, user_id])
        return self.interview_repository.get_interview_by_id(interview_id=interview_id, user_id=user_id)
    
    def update_interview(self, interview_id: int, interview: dict, user_id: int):
        verify_id(id_value=[interview_id, user_id])
        return self.interview_repository.update_interview(
            interview_id=interview_id,
            interview=interview,
            user_id=user_id
        )
    
    def delete_interview(self, interview_id: int, user_id: int):
        verify_id(id_value=[interview_id, user_id])
        return self.interview_repository.delete_interview(interview_id=interview_id, user_id=user_id)
