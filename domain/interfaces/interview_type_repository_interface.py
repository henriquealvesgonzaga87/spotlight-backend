from abc import ABC, abstractmethod
from domain.entities.interview_type import InterviewType


class InterviewTypeRepositoryInterface(ABC):
    @abstractmethod
    async def create_interview_type(self, interview_type: InterviewType):
        pass

    @abstractmethod
    async def get_all_interview_type(self):
        pass
