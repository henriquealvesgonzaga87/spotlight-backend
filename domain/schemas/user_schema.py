from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime


class UserSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: int
    name: str
    email: EmailStr
    password: str
    created_at: datetime
    updated_at: datetime | None


class UserSchemaCreate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    email: EmailStr
    password: str


class UserSchemaUpdate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
