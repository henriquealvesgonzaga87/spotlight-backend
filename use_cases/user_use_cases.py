from domain.interfaces.user_repository_interface import UserRepositoryInterface
from domain.entities.user import User


class UserUseCases:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def create_user(self, user: User):
        return self.user_repository.create_user(user=user)
