from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class InterviewSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: int
    result: str
    interview_date: datetime
    interview_type_id: int
    job_id: int
    created_at: datetime
    updated_at: datetime | None


class InterviewSchemaCreate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    result: str
    interview_date: datetime
    interview_type_id: int
    job_id: int


class InterviewSchemaUpdate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    result: Optional[str] = None
    interview_date: Optional[datetime] = None
    interview_type_id: Optional[int] = None
    job_id: Optional[int] = None
