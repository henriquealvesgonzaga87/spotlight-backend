import pytest


class TestAuthRedisRepo:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    @pytest.mark.asyncio
    async def test_revoke_refresh_token_success(
        self,
        mock_redis_auth_repository_success,
        refresh_token,
        expires_in=7
    ):
        revoked_token = await mock_redis_auth_repository_success.revoke_refresh_token(
            refresh_token=refresh_token,
            expires_in=expires_in
        )

        assert revoked_token is True

    @pytest.mark.asyncio
    async def test_revoke_refresh_token_failure(
        self,
        mock_redis_auth_repository_failure,
        refresh_token,
        expires_in=7
    ):
        with pytest.raises(Exception, match="error"):
            mock_redis_auth_repository_failure.revoke_refresh_token(
                refresh_token=refresh_token,
                expires_in=expires_in
            )
