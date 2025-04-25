from abc import ABC, abstractmethod
from domain.entities.user import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def create_user(self, user: User):
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int):
        pass

    @abstractmethod
    async def update_user(self, user_id, user: User):
        pass

    @abstractmethod
    async def delete_user(self, user_id: int):
        pass
