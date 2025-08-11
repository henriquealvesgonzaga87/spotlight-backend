import re

from domain.exceptions.bad_request_error import BadRequestError
from domain.interfaces.user_repository_interface import UserRepositoryInterface
from domain.entities.user import User
from utils.utils import verify_id


class UserUseCases:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository
        
    def _validate_user_data(self, user: User):
        regex_name = r"^[A-Z][a-zA-Z]{2,}$"

        regex_password = r"^(?=.*[A-Z])(?=.*[@#$%^&+=])(?=.*[a-z])(?=.*[0-9])[A-Za-z\d@#$%^&+=]{8,}$"

        if re.match(regex_name, user.name) is None:
            raise BadRequestError('Name must have at least 2 characters and start with a capital letter')
        
        if re.match(regex_password, user.password) is None:
            raise BadRequestError('Password must contains 8 chars and at least one capital letter, one number and one char between @#$%^&+=')
        
        if user.email == '':
            raise BadRequestError('Email cannot be empty')

    def create_user(self, user: User):
        self._validate_user_data(user=user)
         
        return self.user_repository.create_user(user=user)
    
    def get_user_by_id(self, user_id: int) -> User:
        verify_id(id_value=user_id)
        
        return self.user_repository.get_user_by_id(
            user_id=user_id
        )
    
    def update_user(self, user_id: int, user: User):
        verify_id(id_value=user_id)

        return self.user_repository.update_user(user_id=user_id, user=user)
    
    def delete_user(self, user_id: int):
        verify_id(id_value=user_id)

        return self.user_repository.delete_user(user_id=user_id)
