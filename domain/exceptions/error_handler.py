from fastapi import Request, status
from fastapi.responses import JSONResponse
from domain.exceptions.response_validation_error import ResponseValidationError
from domain.exceptions.integrity_error import IntegrityError

class ErrorHandler:
    @staticmethod
    async def response_validation_error_handler(request: Request, exc: ResponseValidationError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(exc)},
        )
    
    @staticmethod
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": "Integrity error: duplicate entry or constraint violation."}
        )
