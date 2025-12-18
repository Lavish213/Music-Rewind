# LOCATION: backend/src/app/integrations/payments/stripe_webhooks.py
# COMMENT: Stripe webhook verification + event normalization
# NOTE: Pure logic only. No FastAPI, no uvicorn, no HTTP handlers.

from __future__ import annotations

import hmac
import hashlib
import json
import time
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class StripeEventType(str, Enum):
    CHECKOUT_COMPLETED = "checkout.session.completed"
    INVOICE_PAID = "invoice.paid"
    INVOICE_PAYMENT_FAILED = "invoice.payment_failed"
    SUBSCRIPTION_CREATED = "customer.subscription.created"
    SUBSCRIPTION_UPDATED = "customer.subscription.updated"
    SUBSCRIPTION_DELETED = "customer.subscription.deleted"
    UNKNOWN = "unknown"


class StripeSubscriptionStatus(str, Enum):
    ACTIVE = "active"
    TRIALING = "trialing"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    UNPAID = "unpaid"
    INCOMPLETE = "incomplete"
    INVALID = "invalid"


@dataclass(frozen=True)
class StripeEvent:
    """
    Normalized Stripe webhook event.
    """
    event_id: str
    event_type: StripeEventType
    customer_id: Optional[str]
    subscription_id: Optional[str]
    status: Optional[StripeSubscriptionStatus]
    raw: Dict[str, Any]


# -------------------------------------------------------------------
# Signature verification (Stripe-Signature header)
# -------------------------------------------------------------------

def verify_signature(
    *,
    payload: bytes,
    sig_header: str,
    secret: str,
    tolerance_sec: int = 300,
) -> bool:
    """
    Verifies Stripe webhook signature.

    Header format:
    t=timestamp,v1=signature
    """
    try:
        parts = dict(item.split("=", 1) for item in sig_header.split(","))
        timestamp = int(parts.get("t", "0"))
        signature = parts.get("v1")

        if not signature:
            return False

        if abs(time.time() - timestamp) > tolerance_sec:
            logger.warning("Stripe webhook timestamp outside tolerance")
            return False

        signed_payload = f"{timestamp}.{payload.decode()}".encode()
        expected = hmac.new(
            secret.encode(), signed_payload, hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected, signature)

    except Exception as exc:
        logger.error("Stripe signature verification failed: %s", exc)
        return False


# -------------------------------------------------------------------
# Normalization
# -------------------------------------------------------------------

SUBSCRIPTION_STATUS_MAP = {
    "active": StripeSubscriptionStatus.ACTIVE,
    "trialing": StripeSubscriptionStatus.TRIALING,
    "past_due": StripeSubscriptionStatus.PAST_DUE,
    "canceled": StripeSubscriptionStatus.CANCELED,
    "unpaid": StripeSubscriptionStatus.UNPAID,
    "incomplete": StripeSubscriptionStatus.INCOMPLETE,
}


def normalize_event(
    *,
    payload: Dict[str, Any],
) -> StripeEvent:
    """
    Normalizes a Stripe webhook payload into internal representation.
    """
    try:
        event_type_raw = payload.get("type")
        event_type = (
            StripeEventType(event_type_raw)
            if event_type_raw in StripeEventType._value2member_map_
            else StripeEventType.UNKNOWN
        )

        data_object = payload.get("data", {}).get("object", {})

        customer_id = data_object.get("customer")
        subscription_id = data_object.get("subscription") or data_object.get("id")

        status_raw = data_object.get("status")
        status = SUBSCRIPTION_STATUS_MAP.get(
            status_raw, StripeSubscriptionStatus.INVALID
        )

        return StripeEvent(
            event_id=payload.get("id", ""),
            event_type=event_type,
            customer_id=customer_id,
            subscription_id=subscription_id,
            status=status,
            raw=payload,
        )

    except Exception as exc:
        logger.error("Failed to normalize Stripe event: %s", exc)
        return StripeEvent(
            event_id="",
            event_type=StripeEventType.UNKNOWN,
            customer_id=None,
            subscription_id=None,
            status=StripeSubscriptionStatus.INVALID,
            raw=payload,
        )


# -------------------------------------------------------------------
# Convenience entry (used by webhook adapters)
# -------------------------------------------------------------------

def process_webhook(
    *,
    raw_body: bytes,
    headers: Dict[str, str],
    signing_secret: str,
) -> Optional[StripeEvent]:
    """
    Full verification + normalization pipeline.
    """
    sig = headers.get("Stripe-Signature")
    if not sig:
        logger.warning("Missing Stripe-Signature header")
        return None

    if not verify_signature(
        payload=raw_body,
        sig_header=sig,
        secret=signing_secret,
    ):
        logger.warning("Invalid Stripe signature")
        return None

    payload = json.loads(raw_body.decode())