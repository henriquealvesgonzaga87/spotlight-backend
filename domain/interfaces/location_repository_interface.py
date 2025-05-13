from abc import ABC, abstractmethod

from domain.entities.location import City, Country


class LocationRepositoryInterface(ABC):
    @abstractmethod
    async def create_country(self, country: Country):
        pass

    @abstractmethod
    async def create_city(self, city: City):
        pass

    @abstractmethod
    async def create_location(self):
        pass
