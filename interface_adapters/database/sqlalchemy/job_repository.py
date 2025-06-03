from sqlalchemy.orm import Session
from datetime import datetime

from domain.entities.job import Job
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
