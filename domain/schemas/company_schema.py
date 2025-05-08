from pydantic import BaseModel, AnyUrl, ConfigDict
from typing import Optional
from datetime import datetime


class CompanySchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: int
    name: str
    link: AnyUrl | None
    created_at: datetime
    updated_at: datetime | None


class CompanySchemaCreate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    link: Optional[AnyUrl] = None


class CompanySchemaUpdate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: Optional[str] = None
    link: Optional[AnyUrl] = None
