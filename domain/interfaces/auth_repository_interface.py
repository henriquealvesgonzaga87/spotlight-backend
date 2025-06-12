from abc import ABC, abstractmethod

from domain.schemas.auth_schema import LoginSchema


class AuthRepositoryInterface(ABC):

    @abstractmethod
    async def get_user_by_email(self, email: str):
        pass
