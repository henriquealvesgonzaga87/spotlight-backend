from abc import ABC, abstractmethod

from domain.entities.location import City, Country, State


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
    async def create_state(self, state: State):
        pass

    @abstractmethod
    async def create_city(self, city: City):
        pass

    @abstractmethod
    async def create_location(self):
        pass
