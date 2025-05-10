from pydantic import BaseModel


class CitySchema(BaseModel):
    id: int
    name: str
    country_id: int


class CityCreateSchema(BaseModel):
    name: str
    country_id: int
