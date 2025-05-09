from abc import ABC, abstractmethod


class LocationRepositoryInterface(ABC):
    @abstractmethod
    async def create_country(self):
        pass
