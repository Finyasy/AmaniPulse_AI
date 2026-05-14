from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.requests import Request

from app.api.v1.router import api_router
from app.core.abuse import report_rate_limiter
from app.core.config import get_settings
from app.core.errors import error_response, http_exception_handler, validation_exception_handler
from app.core.logging import access_logger, configure_logging
from app.core.observability import request_id_context


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings)
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Anonymous citizen reporting and peace risk guidance API for AmaniPulse AI.",
    )
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )

    @app.middleware("http")
    async def public_abuse_protection_middleware(request: Request, call_next):
        if request.method == "POST" and request.url.path == "/v1/reports":
            content_length = request.headers.get("content-length")
            payload_size = int(content_length) if content_length and content_length.isdigit() else 0
            if content_length is not None and payload_size > settings.max_request_body_bytes:
                return error_response(
                    status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                    code="payload_too_large",
                    message="The report payload is too large.",
                    retryable=False,
                )

            client_key = request.client.host if request.client else "unknown"
            allowed, retry_after = report_rate_limiter.allow(
                key=client_key,
                limit=settings.report_rate_limit_count,
                window_seconds=settings.report_rate_limit_window_seconds,
            )
            if not allowed:
                return error_response(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    code="rate_limited",
                    message="Too many reports were submitted in a short period.",
                    retryable=True,
                    headers={"Retry-After": str(retry_after)},
                )

        return await call_next(request)

    @app.middleware("http")
    async def request_observability_middleware(request: Request, call_next):
        request_id = request.headers.get(settings.request_id_header) or uuid4().hex
        context_token = request_id_context.set(request_id)
        start_time = perf_counter()
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            response.headers[settings.request_id_header] = request_id
            return response
        except Exception:
            access_logger().exception(
                "request_failed",
                extra={
                    "event": "request_failed",
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": status_code,
                    "duration_ms": round((perf_counter() - start_time) * 1000, 2),
                    "environment": settings.environment,
                },
            )
            raise
        finally:
            duration_ms = round((perf_counter() - start_time) * 1000, 2)
            access_logger().info(
                "request_completed",
                extra={
                    "event": "request_completed",
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": status_code,
                    "duration_ms": duration_ms,
                    "environment": settings.environment,
                },
            )
            request_id_context.reset(context_token)

    app.include_router(api_router)
    return app


app = create_app()
