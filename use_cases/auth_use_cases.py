import os

from dotenv import load_dotenv
from datetime import datetime, timedelta
from jose import jwt, ExpiredSignatureError, JWTError

from domain.exceptions.unauthorized_error import UnauthorizedError
from domain.interfaces.auth_repository_interface import AuthRepositoryInterface
from domain.exceptions.bad_request_error import BadRequestError

from domain.interfaces.redis.auth_redis_repository_interface import AuthRedisRepositoryInterface
from domain.schemas.auth_schema import LoginSchema, TokenSchema
from utils.utils import verify


load_dotenv()


class AuthUseCases:
    def __init__(
            self, 
            auth_repository: AuthRepositoryInterface,
            auth_redis_repository: AuthRedisRepositoryInterface
        ):
        self.auth_repository = auth_repository
        self.auth_redis_repository = auth_redis_repository
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
    
    def refresh_token(self, refresh_token: str):
        if not refresh_token:
            raise BadRequestError("Refresh token is required")
        
        try:
            payload = jwt.decode(refresh_token, self.REFRESH_SECRET_KEY, algorithms=self.ALGORITHM)
            email = payload.get("sub")
            access_token = self._create_access_token({"sub": email})
            new_refresh_token = self._create_refresh_token({"sub": email})
            return TokenSchema(access_token=access_token, refresh_token=new_refresh_token)
        
        except ExpiredSignatureError:
            raise UnauthorizedError("Invalid refresh token")
        
        except JWTError:
            raise UnauthorizedError("Invalid refresh token")
        
    def revoke_refresh_token(self, refresh_token: str, expires_in: int):
        if not refresh_token:
            raise BadRequestError("Refresh token is required")
        
        expires_in = int(self.REFRESH_TOKEN_EXPIRE_DAYS) * 24 * 60 * 60  # Default to days in seconds
        if not isinstance(expires_in, int) or expires_in <= 0:
            raise BadRequestError("Expires in must be a positive integer representing seconds")
        
        try:
            return self.auth_redis_repository.revoke_refresh_token(refresh_token, expires_in)
        except Exception as e:
            raise UnauthorizedError(f"Error revoking refresh token: {str(e)}")
        