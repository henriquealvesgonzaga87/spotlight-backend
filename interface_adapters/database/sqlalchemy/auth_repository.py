from sqlalchemy.orm import Session

from domain.entities.user import User
from domain.exceptions.not_found_error import NotFoundError
from domain.interfaces.auth_repository_interface import AuthRepositoryInterface


class SQLAlchemyAuthRepository(AuthRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_email(self, email: str):
        user = self.session.query(User).filter(User.email == email).first()

        if user is None:
            raise NotFoundError(message='User not found with the given email')
        
        return user
