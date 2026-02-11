"""API middleware — authentication, rate limiting, request logging."""
from __future__ import annotations

import time
import uuid
from typing import Any, Callable

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log every request with timing, status, and correlation ID."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        start = time.perf_counter()

        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host if request.client else "unknown",
        )

        try:
            response = await call_next(request)
            duration = time.perf_counter() - start

            logger.info(
                "request_completed",
                status=response.status_code,
                duration_ms=round(duration * 1000, 2),
            )

            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = f"{duration:.4f}"
            return response

        except Exception as e:
            duration = time.perf_counter() - start
            logger.error("request_failed", error=str(e), duration_ms=round(duration * 1000, 2))
            raise
        finally:
            structlog.contextvars.unbind_contextvars("request_id", "method", "path", "client_ip")


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiter per client IP."""

    def __init__(self, app: Any, requests_per_minute: int = 100) -> None:
        super().__init__(app)
        self._limit = requests_per_minute
        self._window = 60
        self._store: dict[str, list[float]] = {}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()

        # Clean old entries
        if client_ip in self._store:
            self._store[client_ip] = [t for t in self._store[client_ip] if now - t < self._window]
        else:
            self._store[client_ip] = []

        if len(self._store[client_ip]) >= self._limit:
            from fastapi.responses import JSONResponse
            retry_after = int(self._window - (now - self._store[client_ip][0]))
            return JSONResponse(
                status_code=429,
                content={
                    "error": {
                        "code": "RATE_LIMITED",
                        "message": f"Rate limit exceeded: {self._limit} requests per {self._window}s",
                    }
                },
                headers={"Retry-After": str(max(1, retry_after))},
            )

        self._store[client_ip].append(now)
        return await call_next(request)


__all__ = ["RequestLoggingMiddleware", "RateLimitMiddleware"]