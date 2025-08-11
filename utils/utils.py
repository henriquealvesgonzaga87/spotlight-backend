from passlib.context import CryptContext

from domain.exceptions.bad_request_error import BadRequestError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def verify_id(id_value: int | list):
    if isinstance(id_value, int):
        if id_value < 0:
            raise BadRequestError("ID must be a positive Integer")
        return
        
    if isinstance(id_value, list):
        for value in id_value:
            if not isinstance(value, int):
                raise BadRequestError("ID must be an Integer")
            
            if value < 0:
                raise BadRequestError("ID must be a positive Integer")
        
        return
            
    else:
        raise BadRequestError("ID must be an Integer")
