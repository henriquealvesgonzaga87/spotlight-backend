from abc import ABC, abstractmethod

from domain.entities.job import Job


class JobRepositoryInterface(ABC):
    @abstractmethod
    async def create_job(self, job: Job):
        pass

    async def get_all_jobs(self):
        pass

    async def get_job_by_id(self, job_id: int):
        pass
