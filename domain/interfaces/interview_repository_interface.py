from abc import ABC, abstractmethod

from domain.entities.interview import Interview


class InterviewRepositoryInterface(ABC):
    @abstractmethod
    async def create_interview(self, interview: Interview):
        pass

    @abstractmethod
    async def get_all_interview(self):
        pass

    @abstractmethod
    async def get_interview_by_id(interview_id: int):
        pass
