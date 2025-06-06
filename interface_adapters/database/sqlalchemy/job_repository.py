from sqlalchemy.orm import Session
from datetime import datetime

from domain.entities.job import Job
from domain.exceptions.not_found_error import NotFoundError
from domain.interfaces.job_repository_interface import JobRepositoryInterface


class SQLAlchemyJobRepository(JobRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def create_job(self, job: Job):
        try:
            job.link = str(job.link) if job.link else None

            job.outcome = str(job.outcome).capitalize() if job.outcome else None

            job.created_at = datetime.utcnow()
            job.updated_at = None

            self.session.add(job)
            self.session.commit()
            self.session.refresh(job)

            return job
        
        except Exception as e:
            self.session.rollback()
            raise(e)
        
        finally:
            self.session.close()

    def get_all_jobs(self):
        jobs = self.session.query(Job).all()

        if len(jobs) == 0:
            raise NotFoundError("Jobs not found")
        
        return jobs
    
    def get_job_by_id(self, job_id: int):
        job = self.session.query(Job).filter(Job.id == job_id).first()

        if job is None:
            raise NotFoundError("Job Not found")
        
        return job
    
    def update_job(self, job_id: int, job: dict):
        query_job = self.get_job_by_id(job_id=job_id)

        try:
            for key, value in job.items():
                if key == "link":
                    value = str(job["link"])
                setattr(query_job, key, value)

            query_job.updated_at = datetime.utcnow()

            self.session.add(query_job)
            self.session.commit()
            self.session.refresh(query_job)

            return query_job
        
        except Exception as e:
            self.session.rollback()
            raise(e)
        
        finally:
            self.session.close()

    def delete_job(self, job_id: int):
        query_job = self.get_job_by_id(job_id=job_id)

        self.session.delete(query_job)
        self.session.commit()

        return query_job
