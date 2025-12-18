from __future__ import annotations

import time
from collections import defaultdict
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.errors import RateLimited


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Basic per-IP rate limiting.

    This is intentionally simple:
    - in-memory
    - process-local
    - good enough for dev / early prod

    Can be replaced later with Redis or API gateway limits.
    """

    def __init__(self, app, max_requests: int = 120, window_sec: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_sec = window_sec
        self.hits = defaultdict(list)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()

        window_start = now - self.window_sec
        hits = self.hits[client_ip]

        # prune old hits
        while hits and hits[0] < window_start:
            hits.pop(0)

        if len(hits) >= self.max_requests:
            raise RateLimited()

        hits.append(now)
        return await call_next(request)