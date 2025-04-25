import pytest
from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError

from domain.entities.user import User
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError
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


    @pytest.mark.asyncio
    async def test_get_user_by_id(self, mock_user_repo_interface_success, user_id=0):
        query_user = await mock_user_repo_interface_success.get_user_by_id(user_id=user_id)

        assert query_user.id == user_id

    
    @pytest.mark.asyncio
    async def test_get_user_by_id_failure(self, mock_user_repo_failure, user_id=99):
        with pytest.raises(NotFoundError, match="Not found with the given parameter"):
            mock_user_repo_failure.get_user_by_id(user_id=user_id)


    @pytest.mark.asyncio
    async def test_update_user(self, mock_user_repo_interface_success, update_user_data, user_id=0):
        updated_user = await mock_user_repo_interface_success.update_user(user=update_user_data, user_id=user_id)

        assert updated_user is not None
        assert updated_user.name == update_user_data.name
        assert updated_user.email == update_user_data.email
        assert updated_user.password == update_user_data.password

        assert isinstance(updated_user, User)


    @pytest.mark.asyncio
    async def test_update_user_failure(self, mock_user_repo_failure, update_user_data, user_id=99):
        with pytest.raises(Exception, match="Not found with the given parameter"):
            mock_user_repo_failure.update_user(user=update_user_data, user_id=user_id)


    @pytest.mark.asyncio
    async def test_delete_user(self, mock_user_repo_interface_success, user_id=0):
        delete_user = await mock_user_repo_interface_success.delete_user(user_id=user_id)

        assert delete_user is True


    @pytest.mark.asyncio
    async def test_delete_user_failure(self, mock_user_repo_failure, user_id=99):
        with pytest.raises(Exception, match="Not found with the given parameter"):
            mock_user_repo_failure.delete_user(user_id=user_id)
