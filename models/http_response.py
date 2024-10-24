from typing import Any, Union
from fastapi import status


class ErrorResponse(Exception):

    def __init__(self, status: int, message: str, details: Any = None):
        self.status = status
        self.message = message
        self.details = details
        super().__init__(self.message)

    @classmethod
    def from_error(cls, e: Union["ErrorResponse", Exception]) -> "ErrorResponse":
        if isinstance(e, cls):
            return e
        return cls(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Internal Server Error",
            "INTERNAL_SERVER_ERROR",
        )
