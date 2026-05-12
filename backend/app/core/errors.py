from typing import Any

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status


def error_payload(
    code: str,
    message: str,
    retryable: bool = False,
) -> dict[str, dict[str, str | bool]]:
    return {
        "error": {
            "code": code,
            "message": message,
            "retryable": retryable,
        }
    }


def error_response(
    status_code: int,
    code: str,
    message: str,
    retryable: bool = False,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        headers=headers,
        content=error_payload(code=code, message=message, retryable=retryable),
    )


async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    detail = exc.detail
    if isinstance(detail, dict):
        code = str(detail.get("code", "http_error"))
        message = str(detail.get("message", "The request could not be completed."))
        retryable = bool(detail.get("retryable", False))
    else:
        code = "http_error"
        message = str(detail)
        retryable = False
    return error_response(
        status_code=exc.status_code,
        code=code,
        message=message,
        retryable=retryable,
        headers=exc.headers,
    )


async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    message = _validation_message(exc.errors())
    return error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        code="validation_error",
        message=message,
        retryable=False,
    )


def _validation_message(errors: list[dict[str, Any]]) -> str:
    if not errors:
        return "Request validation failed."
    first = errors[0]
    location = ".".join(str(item) for item in first.get("loc", []) if item != "body")
    message = str(first.get("msg", "Request validation failed."))
    if location:
        return f"{location}: {message}"
    return message
