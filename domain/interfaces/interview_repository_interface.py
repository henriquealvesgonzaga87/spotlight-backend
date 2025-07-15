from abc import ABC, abstractmethod

from domain.entities.interview import Interview


class InterviewRepositoryInterface(ABC):
    @abstractmethod
    async def create_interview(self, interview: Interview, user_id: int):
        pass

    @abstractmethod
    async def get_all_interview(self, user_id: int):
        pass

    @abstractmethod
    async def get_interview_by_id(self, interview_id: int, user_id: int):
        pass

    @abstractmethod
    async def update_interview(self, interview_id: int, interview: dict):
        pass

    @abstractmethod
    async def delete_interview(self, interview_id: int):
        pass
