# LOCATION: backend/src/app/integrations/storage/blob_store.py
# COMMENT: Unified blob storage interface (local | s3 | gcs)
# GATE: Section 6 – Storage
# NOTE: No FastAPI, no uvicorn, no side effects at import time

from __future__ import annotations

import os
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO, Optional

from app.settings import settings


# ---------------------------------------------------------------------
# Base Interface
# ---------------------------------------------------------------------

class BlobStore(ABC):
    """
    Abstract interface for binary object storage.
    """

    @abstractmethod
    def put(
        self,
        *,
        key: str,
        data: BinaryIO,
        content_type: Optional[str] = None,
    ) -> None:
        pass

    @abstractmethod
    def get(self, *, key: str) -> bytes:
        pass

    @abstractmethod
    def delete(self, *, key: str) -> None:
        pass

    @abstractmethod
    def exists(self, *, key: str) -> bool:
        pass


# ---------------------------------------------------------------------
# Local filesystem implementation (DEV / SAFE DEFAULT)
# ---------------------------------------------------------------------

class LocalBlobStore(BlobStore):
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        return self.base_path / key

    def put(
        self,
        *,
        key: str,
        data: BinaryIO,
        content_type: Optional[str] = None,
    ) -> None:
        path = self._path(key)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "wb") as f:
            shutil.copyfileobj(data, f)

    def get(self, *, key: str) -> bytes:
        path = self._path(key)
        if not path.exists():
            raise FileNotFoundError(key)
        return path.read_bytes()

    def delete(self, *, key: str) -> None:
        path = self._path(key)
        if path.exists():
            path.unlink()

    def exists(self, *, key: str) -> bool:
        return self._path(key).exists()


# ---------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------

def get_blob_store() -> BlobStore:
    """
    Returns the configured blob store based on settings.
    """
    backend = settings.BLOB_BACKEND.lower()

    if backend == "local":
        root = Path(
            os.getenv("BLOB_LOCAL_PATH", "data/blobs")
        )
        return LocalBlobStore(root)

    # Future-proof hooks (not implemented yet)
    if backend == "s3":
        raise NotImplementedError("S3 backend not enabled yet")

    if backend == "gcs":
        raise NotImplementedError("GCS backend not enabled yet")

    raise ValueError(f"Unknown BLOB_BACKEND: {settings.BLOB_BACKEND}")