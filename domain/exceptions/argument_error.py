from domain.exceptions.app_error import AppError


class ArgumentError(AppError):
    def __init__(self, message: str):
        super().__init__(message)
