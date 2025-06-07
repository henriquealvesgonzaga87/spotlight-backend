from abc import ABC, abstractmethod
from domain.entities.interview_type import InterviewType


class InterviewTypeRepositoryInterface(ABC):
    @abstractmethod
    async def create_interview_type(self, interview_type: InterviewType):
        pass

    @abstractmethod
    async def get_all_interview_type(self):
        pass

    @abstractmethod
    async def get_interview_type_by_id(self, interview_type_id: int):
        pass

    @abstractmethod
    async def update_interview_type(self, interview_type_id: int, interview_type: InterviewType):
        pass

    @abstractmethod
    async def delete_interview_type(self, interview_type_id: int):
        pass
