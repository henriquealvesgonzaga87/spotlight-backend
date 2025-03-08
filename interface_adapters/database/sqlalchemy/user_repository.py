from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError
from domain.interfaces.user_repository_interface import UserRepositoryInterface
from domain.entities.user import User
from utils.utils import hash



class SQLAlchemyUserRepository(UserRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session
    
    def create_user(self, user: User) -> User:
        try:
            hash_password = hash(user.password)
            user.password = hash_password
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
    
    def update_user(self, user_id, user: User):
        query_user = self.get_user_by_id(user_id=user_id)

        try:
            query_user.name = user.name
            query_user.email = user.email
            hash_password = hash(user.password)
            query_user.password = hash_password

            self.session.add(query_user)
            self.session.commit()
            self.session.refresh(query_user)

            return query_user
        
        except Exception as e:
            self.session.rollback()
            raise e
        
        finally:
            self.session.close()

    def delete_user(self, user_id: int):
        query_user = self.get_user_by_id(user_id=user_id)

        try:
            self.session.delete(query_user)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()
