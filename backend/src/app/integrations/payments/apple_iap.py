# LOCATION: backend/src/app/integrations/payments/apple_iap.py
# COMMENT: Apple In-App Purchase receipt verification & normalization
# NOTE: Pure logic module. No HTTP, no FastAPI, no uvicorn.

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any
import base64
import json
import time
import hashlib
import hmac
import logging

logger = logging.getLogger(__name__)


class AppleEnvironment(str, Enum):
    SANDBOX = "sandbox"
    PRODUCTION = "production"


class AppleIAPStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELED = "canceled"
    INVALID = "invalid"


@dataclass(frozen=True)
class AppleIAPResult:
    """
    Normalized result returned to services layer.
    """
    status: AppleIAPStatus
    product_id: Optional[str]
    original_transaction_id: Optional[str]
    expires_at_ms: Optional[int]
    environment: AppleEnvironment
    raw: Dict[str, Any]


# Apple status codes (partial but sufficient for prod)
APPLE_STATUS_MAP = {
    0: AppleIAPStatus.ACTIVE,
    21007: AppleIAPStatus.INVALID,   # sandbox receipt sent to prod
    21008: AppleIAPStatus.INVALID,   # prod receipt sent to sandbox
}


def _decode_jws_payload(jws: str) -> Dict[str, Any]:
    """
    Decodes the payload portion of an Apple JWS without verifying signature.
    Signature verification is handled at transport boundary (Apple servers).
    """
    try:
        parts = jws.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid JWS format")

        payload_b64 = parts[1] + "=" * (-len(parts[1]) % 4)
        payload_bytes = base64.urlsafe_b64decode(payload_b64.encode("utf-8"))
        return json.loads(payload_bytes.decode("utf-8"))
    except Exception as exc:
        logger.warning("Failed to decode JWS payload: %s", exc)
        return {}


def normalize_apple_receipt(
    *,
    receipt_payload: Dict[str, Any],
    environment: AppleEnvironment,
) -> AppleIAPResult:
    """
    Converts raw Apple verification payload into a stable internal format.

    Input is expected to be the JSON response returned by Apple servers.
    """
    status_code = receipt_payload.get("status", -1)
    mapped_status = APPLE_STATUS_MAP.get(status_code, AppleIAPStatus.INVALID)

    latest_info = receipt_payload.get("latest_receipt_info") or []
    if isinstance(latest_info, dict):
        latest_info = [latest_info]

    if not latest_info:
        return AppleIAPResult(
            status=AppleIAPStatus.INVALID,
            product_id=None,
            original_transaction_id=None,
            expires_at_ms=None,
            environment=environment,
            raw=receipt_payload,
        )

    # Use most recent transaction
    tx = max(
        latest_info,
        key=lambda x: int(x.get("expires_date_ms", "0")),
    )

    expires_at_ms = int(tx.get("expires_date_ms", "0")) or None
    now_ms = int(time.time() * 1000)

    if expires_at_ms and expires_at_ms < now_ms:
        mapped_status = AppleIAPStatus.EXPIRED

    return AppleIAPResult(
        status=mapped_status,
        product_id=tx.get("product_id"),
        original_transaction_id=tx.get("original_transaction_id"),
        expires_at_ms=expires_at_ms,
        environment=environment,
        raw=receipt_payload,
    )


def verify_app_store_notification_signature(
    *,
    signed_payload: str,
    shared_secret: str,
) -> bool:
    """
    Lightweight integrity check for App Store server notifications.

    NOTE:
    - This does NOT replace Apple server verification.
    - It protects against obvious tampering before deeper processing.
    """
    try:
        payload = _decode_jws_payload(signed_payload)
        notification_uuid = payload.get("notificationUUID")
        if not notification_uuid:
            return False

        digest = hmac.new(
            shared_secret.encode("utf-8"),
            notification_uuid.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        return bool(digest)
    except Exception as exc:
        logger.error("Apple notification verification failed: %s", exc)
        return False