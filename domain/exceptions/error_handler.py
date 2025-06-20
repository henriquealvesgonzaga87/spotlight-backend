from fastapi import status, Request
from fastapi.responses import JSONResponse
from domain.exceptions.argument_error import ArgumentError
from domain.exceptions.bad_request_error import BadRequestError
from domain.exceptions.not_found_error import NotFoundError
from domain.exceptions.response_validation_error import ResponseValidationError
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.unauthorized_error import UnauthorizedError


class ErrorHandler:
    @staticmethod
    def response_validation_error_handler(request: Request, exc: ResponseValidationError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(exc)},
        )
    
    @staticmethod
    def integrity_error_handler(request: Request, exc: IntegrityError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": str(exc)}
        )
    
    @staticmethod
    def not_found_error_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)}
        )
    
    @staticmethod
    def bad_request_error_handler(request: Request, exc: BadRequestError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)}
        )
    
    @staticmethod
    def unauthorized_error_handler(request: Request, exc: UnauthorizedError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)}
        )
    
    @staticmethod
    def argument_error_handler(request: Request, exc: ArgumentError):
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={"message": str(exc)}
        )
