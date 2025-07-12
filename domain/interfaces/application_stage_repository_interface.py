from abc import ABC, abstractmethod

from domain.entities.application_stage import ApplicationStage


class ApplicationStageRepositoryInterface(ABC):
    @abstractmethod
    async def create_application_stage(self, application_stage: ApplicationStage, user_id: int):
        pass

    @abstractmethod
    async def get_all_application_stage(self, user_id: int):
        pass

    @abstractmethod
    async def get_application_stage_by_id(self, application_stage_id: int, user_id: int):
        pass

    @abstractmethod
    async def get_application_stage_by_name(self, application_stage: str, user_id: int):
        pass

    @abstractmethod
    async def get_application_stage_by_name_exactly(self, application_stage: str, user_id: int):
        pass

    @abstractmethod
    async def update_application_stage(self, application_stage: ApplicationStage, application_stage_id: int, user_id: int):
        pass

    @abstractmethod
    async def delete_application_stage(self, application_stage_id: int, user_id: int):
        pass
