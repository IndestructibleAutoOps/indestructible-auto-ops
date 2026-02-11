"""Structured logging configuration — structlog + stdlib integration."""
from __future__ import annotations

import logging
import sys
from typing import Any

import structlog


def setup_logging(
    level: str = "info",
    json_output: bool = False,
    log_file: str | None = None,
) -> None:
    """Configure structlog with stdlib logging integration.

    Args:
        level: Log level string (debug, info, warning, error, critical).
        json_output: If True, output JSON lines; otherwise human-readable.
        log_file: Optional file path for log output in addition to stderr.
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    # --- Shared processors (structlog + stdlib) ---
    shared_processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    if json_output:
        renderer: Any = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(
            colors=sys.stderr.isatty(),
            pad_event=40,
        )

    # --- Configure structlog ---
    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # --- Configure stdlib logging ---
    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
        foreign_pre_chain=shared_processors,
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)

    handlers: list[logging.Handler] = [console_handler]

    # Optional file handler
    if log_file:
        file_formatter = structlog.stdlib.ProcessorFormatter(
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.processors.JSONRenderer(),
            ],
            foreign_pre_chain=shared_processors,
        )
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(file_formatter)
        handlers.append(file_handler)

    # Root logger
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(log_level)
    for handler in handlers:
        root_logger.addHandler(handler)

    # Suppress noisy third-party loggers
    for noisy in ("uvicorn.access", "sqlalchemy.engine", "httpx", "httpcore"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    structlog.get_logger().info(
        "logging_configured",
        level=level,
        json_output=json_output,
        log_file=log_file or "none",
    )


def get_logger(name: str | None = None) -> Any:
    """Get a structlog bound logger."""
    return structlog.get_logger(name)


__all__ = ["setup_logging", "get_logger"]