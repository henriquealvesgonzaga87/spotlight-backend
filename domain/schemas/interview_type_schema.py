from pydantic import BaseModel, ConfigDict
from datetime import datetime


class InterviewTypeSchemaCreate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    interview_type: str


class InterviewTypeSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: int
    interview_type: str
    created_at: datetime
    updated_at: str | None
