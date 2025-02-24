from pydantic import BaseModel, EmailStr, ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: int
    name: str
    email: EmailStr
    password: str


class UserSchemaCreate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    email: EmailStr
    password: str
