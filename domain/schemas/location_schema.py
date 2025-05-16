from pydantic import BaseModel, ConfigDict


class CitySchema(BaseModel):
    id: int
    name: str
    country_id: int


class CityCreateSchema(BaseModel):
    name: str
    country_id: int


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
    country_id: int


class StateCreateSchema(BaseModel):
    name: str
    country_id: int
