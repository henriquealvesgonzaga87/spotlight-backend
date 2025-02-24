from abc import ABC, abstractmethod
from domain.entities.user import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    def create_user(self, user: User):
        pass
