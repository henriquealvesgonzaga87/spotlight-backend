import pytest


class TestAuthRedisRepo:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    @pytest.mark.asyncio
    async def test_revoke_refresh_token_success(
        self,
        mock_redis_auth_repository_success,
        refresh_token_str,
        expires_in=7
    ):
        revoked_token = await mock_redis_auth_repository_success.revoke_refresh_token(
            refresh_token=refresh_token_str,
            expires_in=expires_in
        )

        assert revoked_token is True

    @pytest.mark.asyncio
    async def test_revoke_refresh_token_failure(
        self,
        mock_redis_auth_repository_failure,
        refresh_token_str,
        expires_in=7
    ):
        with pytest.raises(Exception, match="error"):
            mock_redis_auth_repository_failure.revoke_refresh_token(
                refresh_token=refresh_token_str,
                expires_in=expires_in
            )

    @pytest.mark.asyncio
    async def test_is_refresh_token_revoked_success(
        self,
        mock_redis_auth_repository_success,
        refresh_token_str
    ):
        check_revoked_token = await mock_redis_auth_repository_success.is_refresh_token_revoked(
            refresh_token=refresh_token_str
        )

        assert check_revoked_token is not None
        assert check_revoked_token == refresh_token_str

    @pytest.mark.asyncio
    async def test_is_refresh_token_revoked_failure(
        self,
        mock_redis_auth_repository_failure,
        refresh_token_str
    ):
        with pytest.raises(Exception, match="error"):
            mock_redis_auth_repository_failure.is_refresh_token_revoked(
                refresh_token=refresh_token_str
            )
