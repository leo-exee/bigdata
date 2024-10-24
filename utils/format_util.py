from typing import Union

from fastapi.encoders import jsonable_encoder


def format_error_response(
    status: Union[int, str],
    message: str,
    details: list[object] | None = None,
) -> object:
    return {
        "status": status,
        "message": message,
        "details": jsonable_encoder(details),
    }
