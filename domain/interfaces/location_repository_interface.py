from abc import ABC, abstractmethod

from domain.entities.location import City, State


class LocationRepositoryInterface(ABC):
    @abstractmethod
    async def create_country(self):
        pass
    
    @abstractmethod
    async def get_countries(self):
        pass

    @abstractmethod
    async def get_country_by_id(self, country_id: int):
        pass

    @abstractmethod
    async def get_states(self, country_name: str):
        pass

    @abstractmethod
    async def get_state_by_id(self, state_id: int):
        pass

    @abstractmethod
    async def create_state(self, state: State, country_name: str):
        pass

    @abstractmethod
    async def create_city(self,country_name: str, state_name: str, city: City):
        pass

    @abstractmethod
    async def get_cities(self, country_name: str, state_name: str):
        pass

    @abstractmethod
    async def get_city_by_id(self, city_id):
        pass
