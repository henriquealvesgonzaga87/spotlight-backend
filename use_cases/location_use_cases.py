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

    def _validate_id(self, id: int):
        if type(id) != int:
            raise BadRequestError("Country ID must be an integer")
        
        if id < 0:
            raise BadRequestError("Country ID must be a positive integer")
        
    def _validate_city_name(self, city: City):
        regex_name = r"^([A-Z][a-z]{2,}(?:\s[A-Z][a-z]{2,})*)$"

        if re.match(regex_name, city.name) is None:
            raise BadRequestError('Name must have at least 2 characters and start with a capital letter')
        
    def _validate_location_name_for_url(self, name: str):
        chars_to_replace = ["-", "%", "&"]
        for char in chars_to_replace:
            if char in name:
                correct_name = name.replace(char, ' ')
                return correct_name
            
        return name

    def create_country(self):
        return self.location_repository.create_country()
    
    def get_countries(self):
        return self.location_repository.get_countries()
    
    def get_country_by_id(self, country_id: int):
        self._validate_id(id=country_id)
        return self.location_repository.get_country_by_id(country_id=country_id)
    
    def get_states(self, country_name: str):
        correct_name = self._validate_location_name_for_url(name=country_name)
        
        country_name = correct_name

        return self.location_repository.get_states(country_name=country_name)
    
    def get_state_by_id(self, state_id: int):
        self._validate_id(id=state_id)
        return self.location_repository.get_state_by_id(state_id=state_id)
        
    def create_state(self, state: State, country_name: str):
        correct_country_name = self._validate_location_name_for_url(name=country_name)
        return self.location_repository.create_state(state=state.name, country_name=correct_country_name)
    
    def create_city(self, country_name: str, state_name: str, city: City):
        correct_country_name = self._validate_location_name_for_url(name=country_name)
        correct_state_name = self._validate_location_name_for_url(name=state_name)

        return self.location_repository.create_city(country_name=correct_country_name, state_name=correct_state_name, city=city)
    
    def create_location(self):
        return self.location_repository.create_location()
