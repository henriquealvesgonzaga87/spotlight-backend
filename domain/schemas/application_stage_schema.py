from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ApplicationStageSchemaCreate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    application_stage: str
    

class ApplicationStageSchema(BaseModel):
    id: int
    application_stage: str
    created_at: datetime
    updated_at: datetime | None
