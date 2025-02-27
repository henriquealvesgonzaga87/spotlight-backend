from domain.exceptions.app_error import AppError


class IntegrityError(AppError):
    def __init__(self, message: str = "Integrity error"):
        super().__init__(message=message)
