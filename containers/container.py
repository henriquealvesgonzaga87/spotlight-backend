from dependency_injector import containers, providers
from interface_adapters.database.sqlalchemy.application_stage_repository import SQLAlchemyApplicationStageRepository
from interface_adapters.database.sqlalchemy.company_repository import SQLAlchemyCompanyRepository
from interface_adapters.database.sqlalchemy.dependencies import get_db
from interface_adapters.database.sqlalchemy.interview_type_repository import SQLAlchemyInterviewTypeRepository
from interface_adapters.database.sqlalchemy.job_repository import SQLAlchemyJobRepository
from interface_adapters.database.sqlalchemy.location_repository import SQLAlchemyLocationRepository
from interface_adapters.database.sqlalchemy.user_repository import SQLAlchemyUserRepository
from use_cases.application_stage_use_cases import ApplicationStageUseCases
from use_cases.company_use_cases import CompanyUseCases
from use_cases.interview_type_use_cases import InterviewTypeUseCases
from use_cases.job_use_cases import JobUseCases
from use_cases.location_use_cases import LocationUseCases
from use_cases.user_use_cases import UserUseCases
from settings import get_settings


settings = get_settings()

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        "interface_adapters.api.root_routes",
        "interface_adapters.api.user_routes",
        "interface_adapters.api.company_routes",
        "interface_adapters.api.location_routes",
        "interface_adapters.api.application_stage_routes",
        "interface_adapters.api.job_routes",
        "interface_adapters.api.interview_type_routes",
    ])

    data_base_session = providers.Resource(get_db)

    user_repository = providers.Factory(SQLAlchemyUserRepository, session=data_base_session)
    user_use_cases = providers.Factory(UserUseCases, user_repository=user_repository)

    company_repository = providers.Factory(SQLAlchemyCompanyRepository, session=data_base_session)
    company_use_cases = providers.Factory(CompanyUseCases, company_repository=company_repository)

    location_repository = providers.Factory(SQLAlchemyLocationRepository, session=data_base_session)
    location_use_cases = providers.Factory(LocationUseCases, location_repository=location_repository)

    application_stage_repository = providers.Factory(SQLAlchemyApplicationStageRepository, session=data_base_session)
    application_stage_use_cases = providers.Factory(ApplicationStageUseCases, application_stage_repository=application_stage_repository)

    job_repository = providers.Factory(SQLAlchemyJobRepository, session=data_base_session)
    job_use_cases = providers.Factory(JobUseCases, job_respository=job_repository)

    interview_type_repository = providers.Factory(SQLAlchemyInterviewTypeRepository, session=data_base_session)
    interview_type_use_cases = providers.Factory(InterviewTypeUseCases, interview_type_repository=interview_type_repository)
