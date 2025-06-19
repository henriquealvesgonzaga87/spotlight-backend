from abc import ABC, abstractmethod


class AuthRedisRepositoryInterface(ABC):

    @abstractmethod
    async def revoke_refresh_token(self, refresh_token: str, expires_in: int):
        pass

    @abstractmethod
    async def is_refresh_token_revoked(self, refresh_token: str):
        pass
