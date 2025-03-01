from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError
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
        except SQLAlchemyIntegrityError as e:
            self.session.rollback()
            raise IntegrityError(str(e))
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def get_user_by_id(self, user_id: int) -> User:
        user = self.session.query(User).filter(User.id == user_id).first()

        if user is None:
            raise NotFoundError(message='Not found with the given parameter')
        
        return user
