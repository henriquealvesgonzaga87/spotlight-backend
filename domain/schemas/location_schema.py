from pydantic import BaseModel


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
