from domain.interfaces.user_repository_interface import UserRepositoryInterface
from domain.entities.user import User


class UserUseCases:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

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
