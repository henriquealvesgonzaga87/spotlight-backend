from domain.entities.job import Job
from domain.exceptions.bad_request_error import BadRequestError
from domain.interfaces.job_repository_interface import JobRepositoryInterface
from utils.utils import verify_id


class JobUseCases:
    def __init__(self, job_respository: JobRepositoryInterface):
        self.job_repository = job_respository
    
    def create_job(self, job: Job):
        return self.job_repository.create_job(job=job)
    
    def get_all_jobs(self, user_id: int):
        verify_id(id_value=user_id)
        return self.job_repository.get_all_jobs(user_id=user_id)
    
    def get_job_by_id(self, job_id: int, user_id: int):
        verify_id(id_value=[job_id, user_id])
        return self.job_repository.get_job_by_id(job_id=job_id, user_id=user_id)
    
    def update_job(self, job_id: int, job: dict, user_id: int):
        verify_id(id_value=[job_id, user_id])
        return self.job_repository.update_job(
            job_id=job_id,
            job=job,
            user_id=user_id
        )
    
    def delete_job(self, job_id: int, user_id: int):
        verify_id(id_value=[job_id, user_id])
        return self.job_repository.delete_job(job_id=job_id, user_id=user_id)
    