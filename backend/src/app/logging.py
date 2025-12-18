from __future__ import annotations

import logging
import sys
from typing import Optional


def configure_logging(level: Optional[str] = None) -> None:
    """
    Configure application-wide logging.

    - Single stdout handler (container-friendly)
    - Consistent format
    - Safe defaults for dev/prod
    """
    log_level = (level or "INFO").upper()

    root = logging.getLogger()
    root.setLevel(log_level)

    # Clear existing handlers to avoid duplicate logs (e.g., reloads)
    while root.handlers:
        root.handlers.pop()

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)

    # Reduce noisy third-party logs
    for noisy in ("uvicorn.access", "httpx"):
        logging.getLogger(noisy).setLevel(logging.WARNING)