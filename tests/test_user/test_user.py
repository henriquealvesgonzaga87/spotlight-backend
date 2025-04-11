import pytest
from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError

from domain.entities.user import User
from domain.exceptions.integrity_error import IntegrityError
from domain.schemas.user_schema import UserSchema

class TestUser:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    @pytest.mark.asyncio
    async def test_create_user(self, create_user_data, mock_user_repo_interface_success):
        new_user = await mock_user_repo_interface_success.create_user(user=create_user_data)

        assert new_user is not None
        assert new_user.name == create_user_data.name
        assert new_user.email == create_user_data.email
        assert new_user.password == create_user_data.password

        assert isinstance(new_user, User)


    @pytest.mark.asyncio
    async def test_create_user_failure(self, create_user_data, mock_user_repo_failure):
        with pytest.raises(IntegrityError, match="Integrity error occurred"):
            mock_user_repo_failure.create_user(user=create_user_data)
