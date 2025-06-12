import os

from dotenv import load_dotenv
from datetime import datetime, timedelta
from jose import jwt

from domain.exceptions.unauthorized_error import UnauthorizedError
from domain.interfaces.auth_repository_interface import AuthRepositoryInterface
from domain.exceptions.bad_request_error import BadRequestError

from domain.schemas.auth_schema import LoginSchema, TokenSchema
from utils.utils import verify


load_dotenv()


class AuthUseCases:
    def __init__(self, auth_repository: AuthRepositoryInterface):
        self.auth_repository = auth_repository
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
        self.REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")

    def get_user_by_email(self, email:str):
        if email is None or not isinstance(email, str):
            raise BadRequestError("Email cannot be empty and must be a string")
        
        return self.auth_repository.get_user_by_email(email=email)
    
    def _authenticate_user(self, email:str, password:str):
        user = self.get_user_by_email(email=email)

        if not verify(plain_password=password, hashed_password=user.password):
            raise UnauthorizedError("Incorrect email or password")
        
        return user

    def _create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=int(self.ACCESS_TOKEN_EXPIRE_MINUTES)))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def _create_refresh_token(self, data: dict):
        expire = datetime.utcnow() + timedelta(days=int(self.REFRESH_TOKEN_EXPIRE_DAYS))
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.REFRESH_SECRET_KEY, algorithm=self.ALGORITHM)

    def login(self, login_data: LoginSchema):
        user = self._authenticate_user(login_data.email, login_data.password)
        if not user:
            return None
        access_token = self._create_access_token({"sub": user.email})
        refresh_token = self._create_refresh_token({"sub": user.email})
        return TokenSchema(
            access_token=access_token, 
            refresh_token=refresh_token
        )    
