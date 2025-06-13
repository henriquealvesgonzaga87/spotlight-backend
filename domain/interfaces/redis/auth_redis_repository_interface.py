from abc import ABC, abstractmethod


class AuthRedisRepositoryInterface(ABC):

    @abstractmethod
    async def revoke_refresh_token(self, refresh_token: str, expires_in: int):
        pass