from domain.interfaces.redis.auth_redis_repository_interface import AuthRedisRepositoryInterface



class RedisAuthRepository(AuthRedisRepositoryInterface):
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def revoke_refresh_token(self, refresh_token: str, expires_in: int):
        try:
            self.redis_client.set(refresh_token, "revoked", ex=expires_in)
            return True
        except Exception as e:
            raise Exception(f"Error revoking refresh token: {str(e)}")
        
    def is_refresh_token_revoked(self, refresh_token):
        try:
            return self.redis_client.get(refresh_token) is not None
        except Exception as e:
            raise Exception(f"Error checking refresh token status: {str(e)}")
