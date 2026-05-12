import json
import logging
import sys
from typing import Any

from app.core.config import Settings

ACCESS_LOGGER_NAME = "amanipulse.access"


class JsonLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for key in (
            "event",
            "request_id",
            "method",
            "path",
            "status_code",
            "duration_ms",
            "environment",
        ):
            value = getattr(record, key, None)
            if value is not None:
                payload[key] = value
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, separators=(",", ":"), default=str)


def configure_logging(settings: Settings) -> None:
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    if settings.log_format.lower() == "json":
        handler.setFormatter(JsonLogFormatter())
    else:
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s %(name)s %(message)s",
            )
        )

    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(level)
    logging.getLogger(ACCESS_LOGGER_NAME).setLevel(level)


def access_logger() -> logging.Logger:
    return logging.getLogger(ACCESS_LOGGER_NAME)
