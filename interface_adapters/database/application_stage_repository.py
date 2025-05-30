from datetime import datetime
from sqlalchemy.orm import Session

from domain.entities.application_stage import ApplicationStage
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError
from domain.interfaces.application_stage_repository_interface import ApplicationStageRepositoryInterface


class SQLAlchemyApplicationStageRepository(ApplicationStageRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def create_application_stage(self, application_stage: ApplicationStage):
        try:
            application_stage.created_at = datetime.utcnow()
            application_stage.updated_at = None

            self.session.add(application_stage)
            self.session.commit()
            self.session.refresh(application_stage)

            return application_stage
        
        except IntegrityError as e:
            self.session.rollback()
            raise IntegrityError("UNIQUE constraint failed")
        
        finally:
            self.session.close()

    def get_all_application_stage(self):
        application_stage = self.session.query(ApplicationStage).all()

        if len(application_stage) == 0:
            raise NotFoundError("No Application stage registered")
        
        return application_stage
