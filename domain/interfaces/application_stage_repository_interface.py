from abc import ABC, abstractmethod

from domain.entities.application_stage import ApplicationStage


class ApplicationStageRepositoryInterface(ABC):
    @abstractmethod
    async def create_application_stage(self, application_stage: ApplicationStage):
        pass
