from domain.entities.job import Job
from domain.interfaces.job_repository_interface import JobRepositoryInterface


class JobUseCases:
    def __init__(self, job_respository: JobRepositoryInterface):
        self.job_repository = job_respository
    
    def create_job(self, job: Job):
        return self.job_repository.create_job(job=job)
    
    def get_all_jobs(self):
        return self.job_repository.get_all_jobs()
    