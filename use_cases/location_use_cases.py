from dotenv import load_dotenv

from domain.entities.location import City, State
from domain.interfaces.location_repository_interface import LocationRepositoryInterface
from utils.utils import verify_id


load_dotenv()


class LocationUseCases:
    def __init__(self, location_repository: LocationRepositoryInterface):
        self.location_repository = location_repository
        
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
        verify_id(id_value=country_id)
        return self.location_repository.get_country_by_id(country_id=country_id)
    
    def get_states(self, country_name: str):
        correct_name = self._validate_location_name_for_url(name=country_name)
        
        country_name = correct_name

        return self.location_repository.get_states(country_name=country_name)
    
    def get_state_by_id(self, state_id: int):
        verify_id(id_value=state_id)
        return self.location_repository.get_state_by_id(state_id=state_id)
        
    def create_state(self, state: State):
        return self.location_repository.create_state(state=state)
    
    def create_city(self, country_name: str, state_name: str, city: City):
        correct_country_name = self._validate_location_name_for_url(name=country_name)
        correct_state_name = self._validate_location_name_for_url(name=state_name)

        return self.location_repository.create_city(country_name=correct_country_name, state_name=correct_state_name, city=city)
    
    def get_cities(self, country_name: str, state_name: str):
        correct_country_name = self._validate_location_name_for_url(name=country_name)
        correct_state_name = self._validate_location_name_for_url(name=state_name)

        return self.location_repository.get_cities(country_name=correct_country_name, state_name=correct_state_name)
    
    def get_city_by_id(self, city_id: int):
        verify_id(id_value=city_id)
        return self.location_repository.get_city_by_id(city_id=city_id)
