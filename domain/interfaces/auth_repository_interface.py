from abc import ABC, abstractmethod


class AuthRepositoryInterface(ABC):

    @abstractmethod
    async def get_user_by_email(self, email: str):
        pass
