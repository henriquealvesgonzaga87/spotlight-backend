from sqlalchemy.orm import Session
from domain.interfaces.user_repository_interface import UserRepositoryInterface
from domain.entities.user import User


class SQLAlchemyUserRepository(UserRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session
    
    def create_user(self, user: User) -> User:
        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except Exception as e:
            self.session.rollback()
            return e
        finally:
            self.session.close()
