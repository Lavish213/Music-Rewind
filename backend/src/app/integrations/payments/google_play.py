# LOCATION: backend/src/app/integrations/payments/google_play.py
# COMMENT: Google Play subscription / purchase verification normalization
# NOTE: Pure logic module. No HTTP, no FastAPI, no uvicorn.

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any
import time
import logging

logger = logging.getLogger(__name__)


class GooglePlayEnvironment(str, Enum):
    PRODUCTION = "production"


class GooglePlayStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELED = "canceled"
    PAUSED = "paused"
    GRACE_PERIOD = "grace_period"
    INVALID = "invalid"


@dataclass(frozen=True)
class GooglePlayResult:
    """
    Normalized subscription or one-time purchase state.
    """
    status: GooglePlayStatus
    product_id: Optional[str]
    order_id: Optional[str]
    expires_at_ms: Optional[int]
    raw: Dict[str, Any]


# Google subscription states (per official API)
SUBSCRIPTION_STATE_MAP = {
    "SUBSCRIPTION_STATE_ACTIVE": GooglePlayStatus.ACTIVE,
    "SUBSCRIPTION_STATE_IN_GRACE_PERIOD": GooglePlayStatus.GRACE_PERIOD,
    "SUBSCRIPTION_STATE_CANCELED": GooglePlayStatus.CANCELED,
    "SUBSCRIPTION_STATE_PAUSED": GooglePlayStatus.PAUSED,
    "SUBSCRIPTION_STATE_EXPIRED": GooglePlayStatus.EXPIRED,
}


def normalize_subscription_response(
    *,
    subscription_payload: Dict[str, Any],
) -> GooglePlayResult:
    """
    Normalizes Google Play subscription API response.

    Input is the raw JSON returned by:
    purchases.subscriptionsv2.get
    """
    try:
        product_id = subscription_payload.get("lineItems", [{}])[0].get("productId")
        order_id = subscription_payload.get("orderId")

        expiry_time = subscription_payload.get("lineItems", [{}])[0].get(
            "expiryTime", {}
        ).get("seconds")

        expires_at_ms = (
            int(expiry_time) * 1000 if isinstance(expiry_time, str) else None
        )

        state_key = subscription_payload.get("subscriptionState")
        mapped_status = SUBSCRIPTION_STATE_MAP.get(
            state_key, GooglePlayStatus.INVALID
        )

        if expires_at_ms:
            now_ms = int(time.time() * 1000)
            if expires_at_ms < now_ms:
                mapped_status = GooglePlayStatus.EXPIRED

        return GooglePlayResult(
            status=mapped_status,
            product_id=product_id,
            order_id=order_id,
            expires_at_ms=expires_at_ms,
            raw=subscription_payload,
        )

    except Exception as exc:
        logger.error("Failed to normalize Google Play subscription: %s", exc)
        return GooglePlayResult(
            status=GooglePlayStatus.INVALID,
            product_id=None,
            order_id=None,
            expires_at_ms=None,
            raw=subscription_payload,
        )


def normalize_one_time_purchase(
    *,
    purchase_payload: Dict[str, Any],
) -> GooglePlayResult:
    """
    Normalizes Google Play one-time purchase verification response.
    """
    try:
        purchase_state = purchase_payload.get("purchaseState")
        acknowledged = purchase_payload.get("acknowledgementState") == 1

        status = (
            GooglePlayStatus.ACTIVE
            if purchase_state == 0 and acknowledged
            else GooglePlayStatus.CANCELED
        )

        return GooglePlayResult(
            status=status,
            product_id=purchase_payload.get("productId"),
            order_id=purchase_payload.get("orderId"),
            expires_at_ms=None,
            raw=purchase_payload,
        )

    except Exception as exc:
        logger.error("Failed to normalize Google Play purchase: %s", exc)
        return GooglePlayResult(
            status=GooglePlayStatus.INVALID,
            product_id=None,
            order_id=None,
            expires_at_ms=None,
            raw=purchase_payload,
        )