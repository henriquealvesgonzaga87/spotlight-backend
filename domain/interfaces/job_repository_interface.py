from abc import ABC, abstractmethod

from domain.entities.job import Job


class JobRepositoryInterface(ABC):
    @abstractmethod
    async def create_job(self, job: Job):
        pass
