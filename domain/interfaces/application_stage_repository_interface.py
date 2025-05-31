from abc import ABC, abstractmethod

from domain.entities.application_stage import ApplicationStage


class ApplicationStageRepositoryInterface(ABC):
    @abstractmethod
    async def create_application_stage(self, application_stage: ApplicationStage):
        pass

    @abstractmethod
    async def get_all_application_stage(self):
        pass

    @abstractmethod
    async def get_application_stage_by_id(self, application_stage_id: int):
        pass

    @abstractmethod
    async def update_application_stage(self, application_stage: ApplicationStage, application_stage_id: int):
        pass
