from abc import ABC, abstractmethod

from domain.entities.location import City


class LocationRepositoryInterface(ABC):
    @abstractmethod
    async def create_country(self):
        pass

    @abstractmethod
    async def create_city(self, city: City):
        pass

    @abstractmethod
    async def create_location(self):
        pass
