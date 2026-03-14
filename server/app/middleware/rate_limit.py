import logging
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Stub rate-limiting middleware — implementation to be added when needed."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Response]
    ) -> Response:
        """Pass requests through without rate limiting until implemented."""
        logger.debug("RateLimitMiddleware: passing request through")
        return await call_next(request)
