from abc import ABC, abstractmethod

from domain.entities.interview import Interview


class InterviewRepositoryInterface(ABC):
    @abstractmethod
    async def create_interview(self, interview: Interview):
        pass
