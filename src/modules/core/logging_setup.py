from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    from structlog.types import Processor

log = structlog.get_logger(__name__)

OWN_PACKAGES = ("src",)


SKIP_ACCESS_LOG_PATHS = (
    "/health ",
    "/healthz ",
    "/health/live ",
    "/health/ready ",
    "/metrics ",
)


class DropNoisyAccessFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        return not any(path in msg for path in SKIP_ACCESS_LOG_PATHS)


def setup_logging(environment: str, debug: bool = False) -> None:
    renderer: Processor = (
        structlog.dev.ConsoleRenderer() if environment == "dev" else structlog.processors.JSONRenderer()
    )

    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.ExceptionRenderer(),
        renderer,
    ]

    structlog.configure(
        processors=shared_processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.WARNING,
    )

    log_level = logging.DEBUG if debug else logging.INFO
    for package in OWN_PACKAGES:
        logging.getLogger(package).setLevel(log_level)
        logging.getLogger(f"src.{package}").setLevel(log_level)

    access_logger = logging.getLogger("uvicorn.access")
    access_logger.setLevel(logging.INFO)
    access_logger.addFilter(DropNoisyAccessFilter())
