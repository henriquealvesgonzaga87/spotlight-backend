import os
import re
import requests

from dotenv import load_dotenv

from domain.entities.location import City, Country, State
from domain.exceptions.bad_request_error import BadRequestError
from domain.interfaces.location_repository_interface import LocationRepositoryInterface


load_dotenv()


class LocationUseCases:
    def __init__(self, location_repository: LocationRepositoryInterface):
        self.location_repository = location_repository
        self._API_COUNTRIES = os.getenv("API_COUNTRIES")

    def _validate_country_id(self, country_id: int):
        if type(country_id) != int:
            raise BadRequestError("Country ID must be an integer")
        
        if country_id < 0:
            raise BadRequestError("Country ID must be a positive integer")
        
    def _validate_city_name(self, city: City):
        regex_name = r"^([A-Z][a-z]{2,}(?:\s[A-Z][a-z]{2,})*)$"

        if re.match(regex_name, city.name) is None:
            raise BadRequestError('Name must have at least 2 characters and start with a capital letter')

    def create_country(self):
        return self.location_repository.create_country()
        
    def create_state(self, state: State):
        self.location_repository.create_state(state=state)
    
    def create_city(self, city: City):
        self._validate_country_id(country_id=city.country_id)
        self._validate_city_name(city=city)

        return self.location_repository.create_city(city=city)
    
    def create_location(self):
        return self.location_repository.create_location()
