from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import ArgumentError as SQLArgumentError

from domain.entities.application_stage import ApplicationStage
from domain.entities.job import Job
from domain.exceptions.argument_error import ArgumentError
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError
from domain.interfaces.application_stage_repository_interface import ApplicationStageRepositoryInterface


class SQLAlchemyApplicationStageRepository(ApplicationStageRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def create_application_stage(self, application_stage: ApplicationStage):
        try:
            application_stage.application_stage = str(application_stage.application_stage).lower()
            application_stage.created_at = datetime.utcnow()
            application_stage.updated_at = None

            query_application_stage = self.get_application_stage_by_name_exactly(application_stage=application_stage.application_stage)

            if query_application_stage:
                return query_application_stage

            self.session.add(application_stage)
            self.session.commit()
            self.session.refresh(application_stage)

            return application_stage
        
        except IntegrityError as e:
            self.session.rollback()
            raise IntegrityError("UNIQUE constraint failed")
        
        finally:
            self.session.close()

    def get_all_application_stage(self, user_id: int):
        application_stage = self.session.query(ApplicationStage)\
            .join(ApplicationStage.job)\
            .filter(Job.user_id == user_id)\
            .all()

        if len(application_stage) == 0:
            raise NotFoundError("No Application stage registered")
        
        return application_stage
    
    def get_application_stage_by_id(self, application_stage_id: int):
        application_stage = self.session.query(ApplicationStage).filter(ApplicationStage.id == application_stage_id).first()

        if application_stage is None:
            raise NotFoundError("Application stage not found with the given ID")
        
        return application_stage
    
    def get_application_stage_by_name(self, application_stage: str):
        try:
            query_application_stage = self.session.query(ApplicationStage).filter(
                ApplicationStage.application_stage.ilike(f"%{application_stage}%")).all()
            
            if len(query_application_stage) == 0:
                raise NotFoundError("Not found with the given name")
            
            return query_application_stage

        except SQLArgumentError:
            raise ArgumentError("something went wrong, please try again.")
        
    def get_application_stage_by_name_exactly(self, application_stage: str):
        query_application_stage = self.session.query(ApplicationStage).filter(
            ApplicationStage.application_stage == application_stage.lower()
        ).first()
        
        return query_application_stage
    
    def update_application_stage(self, application_stage: ApplicationStage, application_stage_id: int):
        query_application_stage = self.get_application_stage_by_id(
            application_stage_id=application_stage_id
        )

        try:
            query_application_stage.application_stage = application_stage.application_stage
            query_application_stage.updated_at = datetime.utcnow()

            self.session.add(query_application_stage)
            self.session.commit()
            self.session.refresh(query_application_stage)

            return query_application_stage

        except IntegrityError as e:
            self.session.rollback()
            raise IntegrityError("UNIQUE constraint failed")
        
        finally:
            self.session.close()

    def delete_application_stage(self, application_stage_id: int):
        try:
            query_application_stage = self.get_application_stage_by_id(
                application_stage_id=application_stage_id
            )

            self.session.delete(query_application_stage)
            self.session.commit()

            return query_application_stage
        
        except NotFoundError as e:
            raise NotFoundError("Application stage not found with the given ID")
        
        finally:
            self.session.close()
