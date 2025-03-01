from domain.interfaces.user_repository_interface import UserRepositoryInterface
from domain.entities.user import User


class UserUseCases:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def validate_user_id(self, user_id):
        if type(user_id) != int:
            raise ValueError("The given ID must be an integer")
        
        if user_id is None:
            raise ValueError("ID cannot be empty")

    def create_user(self, user: User):
        if len(user.name) < 2:
            raise ValueError('Name must have at least 2 characters')
        if user.name == '':
            raise ValueError('Name cannot be empty')
        if user.email == '':
            raise ValueError('Email cannot be empty')
        if user.password == '':
            raise ValueError('Password cannot be empty')
         
        return self.user_repository.create_user(user=user)
    
    def get_user_by_id(self, user_id: int) -> User:
        self.validate_user_id(user_id=user_id)
        
        return self.user_repository.get_user_by_id(user_id=user_id)
    
    def update_user(self, user_id: int, user: User):
        self.validate_user_id(user_id=user_id)

        return self.user_repository.update_user(user_id=user_id, user=user)
