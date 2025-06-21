import pytest

from domain.entities.user import User
from domain.exceptions.not_found_error import NotFoundError


class TestAuthSQLRepo:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    @pytest.mark.asyncio
    async def test_get_user_by_email_success(
        self,
        mock_auth_repository_success,
        email="test@mail.com"
    ):
        user = await mock_auth_repository_success.get_user_by_email(
            email=email
        )

        assert user is not None
        assert user.email == email
        assert isinstance(user, User)

    @pytest.mark.asyncio
    async def test_get_user_by_email_failure(
        self,
        mock_auth_repository_failure,
        email="failure@mail.com"
    ):
        with pytest.raises(NotFoundError, match="error"):
            mock_auth_repository_failure.get_user_by_email(
                email=email
            )
