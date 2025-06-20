from pydantic import BaseModel, AnyUrl, ConfigDict
from typing import Optional
from datetime import datetime, date


class JobSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: int
    name: str
    link: AnyUrl | None
    application_date: date | None
    application_stage_id: int
    outcome: str | None
    user_id: int
    company_id: int
    country_id: int
    state_id: int
    city_id: int
    created_at: datetime | None
    updated_at: datetime | None


class JobSchemaCreate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    link: Optional[AnyUrl] = None
    application_date: Optional[date] = None
    application_stage_id: int
    outcome: Optional[str] = None
    user_id: Optional[int] = None
    company_id: int
    country_id: int
    state_id: int
    city_id: int


class JobSchemaUpdate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: Optional[str] = None
    link: Optional[AnyUrl] = None
    application_date: Optional[date] = None
    application_stage_id: Optional[int] = None
    outcome: Optional[str] = None
    user_id: Optional[int] = None
    company_id: Optional[int] = None
    country_id: Optional[int] = None
    state_id: Optional[int] = None
    city_id: Optional[int] = None
