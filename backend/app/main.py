from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from app.api.v1.router import api_router
from app.core.config import get_settings
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

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )

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
