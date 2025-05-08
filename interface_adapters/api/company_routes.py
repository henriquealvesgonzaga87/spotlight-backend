from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Body

from domain.entities.company import Company
from domain.schemas.company_schema import CompanySchema, CompanySchemaCreate, CompanySchemaUpdate
from containers.container import Container
from use_cases.company_use_cases import CompanyUseCases


router = APIRouter()


@router.post("/company", status_code=status.HTTP_201_CREATED, response_model=CompanySchema)
@inject
def create_company(company_data: CompanySchemaCreate = Body(...), company_use_cases: CompanyUseCases = Depends(Provide[Container.company_use_cases])):
    company = company_use_cases.create_company(
        Company(
            name=company_data.name,
            link=company_data.link
        ))
    company_json = jsonable_encoder(obj=company)


    return company_json


@router.get("/company/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanySchema)
@inject
def get_company_by_id(company_id: int, company_use_case: CompanyUseCases = Depends(Provide[Container.company_use_cases])):
    company = company_use_case.get_company_by_id(company_id=company_id)
    company_json = jsonable_encoder(obj=company)

    return company_json


@router.get("/company", status_code=status.HTTP_200_OK, response_model=list[CompanySchema])
@inject
def get_all_companies(company_use_case: CompanyUseCases = Depends(Provide[Container.company_use_cases])):
    companies = company_use_case.get_all_companies()
    companies_json = jsonable_encoder(obj=companies)

    return companies_json


@router.patch("/company/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanySchema)
@inject
def update_company(company_id: int, company_data: CompanySchemaUpdate = Body(...), company_use_cases: CompanyUseCases = Depends(Provide[Container.company_use_cases])):
    company = company_use_cases.update_company(
        company_id=company_id,
        company=Company(
            name=company_data.name,
            link=company_data.link,
        )
    )
    company_json = jsonable_encoder(company)

    return company_json


@router.delete("/company/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_company(company_id: int, company_use_cases: CompanyUseCases = Depends(Provide[Container.company_use_cases])):
    company = company_use_cases.delete_company(company_id=company_id)

    return {"message": f"{company.name} deleted successfully"}
