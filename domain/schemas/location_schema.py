from pydantic import BaseModel, ConfigDict


class CitySchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: int | None
    name: str
    state_id: int | None


class CityCreateSchema(BaseModel):
    name: str


class CountryCreateSchema(BaseModel):
    common_name: str


class CountrySchema(BaseModel):
    id: int
    common_name: str
    code: str


class StateSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: int | None
    name: str
    code: str
    admin_code: int
    country_id: int


class StateCreateSchema(BaseModel):
    name: str
    country_id: int
