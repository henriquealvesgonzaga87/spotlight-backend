from abc import ABC, abstractmethod

from domain.entities.job import Job


class JobRepositoryInterface(ABC):
    @abstractmethod
    async def create_job(self, job: Job):
        pass

    @abstractmethod
    async def get_all_jobs(self, user_id: int):
        pass

    @abstractmethod
    async def get_job_by_id(self, job_id: int, user_id: int):
        pass

    @abstractmethod
    async def update_job(self, job_id: int, job: dict, user_id: int):
        pass

    @abstractmethod
    async def delete_job(self, job_id: int, user_id: int):
        pass
