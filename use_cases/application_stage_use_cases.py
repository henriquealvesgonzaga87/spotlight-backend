import re

from domain.entities.application_stage import ApplicationStage
from domain.exceptions.bad_request_error import BadRequestError
from domain.interfaces.application_stage_repository_interface import ApplicationStageRepositoryInterface


class ApplicationStageUseCases:
    def __init__(self, application_stage_repository: ApplicationStageRepositoryInterface):
        self.application_stage_repository = application_stage_repository

    def _validate_application_stage_data(self, string):
        regex_string = r"^[A-Z][a-zA-ZÀ-ÿ]{2,}(?:\s[a-zA-ZÀ-ÿ]{3,})*$"

        if re.match(regex_string, string) is None:
            raise BadRequestError('Application Stage must have at least 2 characters and start with a capital letter')

    def _validate_id(self, id: int):
        if id < 0:
            raise BadRequestError("ID must be a positive Integer")
        
        if not isinstance(id, int):
            raise BadRequestError("ID must be an Integer")

    def create_application_stage(self, application_stage: ApplicationStage):
        self._validate_application_stage_data(string=application_stage.application_stage)

        return self.application_stage_repository.create_application_stage(
            application_stage=application_stage
        )
    
    def get_all_application_stage(self):
        return self.application_stage_repository.get_all_application_stage()
    
    def get_application_stage_by_id(self, application_stage_id: int):
        self._validate_id(id=application_stage_id)
        return self.application_stage_repository.get_application_stage_by_id(
            application_stage_id=application_stage_id
        )
    
    def get_application_stage_by_name(self, application_stage: str):
        return self.application_stage_repository.get_application_stage_by_name(
            application_stage=application_stage
        )
    
    def get_application_stage_by_name_exactly(self, application_stage: str):
        return self.application_stage_repository.get_application_stage_by_name_exactly(
            application_stage=application_stage
        )
    
    def update_application_stage(self, application_stage: ApplicationStage, application_stage_id: int):
        self._validate_id(id=application_stage_id)
        self._validate_application_stage_data(string=application_stage.application_stage)
        return self.application_stage_repository.update_application_stage(
            application_stage=application_stage,
            application_stage_id=application_stage_id
        )
    
    def delete_application_stage(self, application_stage_id: int):
        self._validate_id(id=application_stage_id)
        return self.application_stage_repository.delete_application_stage(
            application_stage_id=application_stage_id
        )
