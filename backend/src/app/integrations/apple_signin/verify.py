# LOCATION: backend/src/app/integrations/apple_signin/verify.py
# COMMENT: Verify Apple identity token (id_token) via Apple's JWKS

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any, Optional
from urllib.request import urlopen

import jwt  # PyJWT


APPLE_JWKS_URL = "https://appleid.apple.com/auth/keys"


class AppleTokenError(Exception):
    pass


@dataclass(frozen=True)
class AppleClaims:
    sub: str
    email: Optional[str]
    email_verified: Optional[bool]
    iss: str
    aud: str
    iat: int
    exp: int


class _JWKSCache:
    def __init__(self, ttl_seconds: int = 60 * 60):
        self.ttl_seconds = ttl_seconds
        self._jwks: Optional[dict[str, Any]] = None
        self._loaded_at: float = 0.0

    def get(self) -> dict[str, Any]:
        now = time.time()
        if self._jwks is None or (now - self._loaded_at) > self.ttl_seconds:
            with urlopen(APPLE_JWKS_URL, timeout=10) as resp:
                payload = resp.read().decode("utf-8")
                self._jwks = json.loads(payload)
                self._loaded_at = now
        return self._jwks


_jwks_cache = _JWKSCache()


def verify_apple_id_token(
    id_token: str,
    *,
    audience: str,
    issuer: str = "https://appleid.apple.com",
    leeway_seconds: int = 30,
) -> AppleClaims:
    """
    Verifies an Apple Sign-In id_token using Apple's public keys (JWKS).

    - audience: your Apple Services ID / Bundle ID (what Apple sets as aud)
    """
    if not id_token or not isinstance(id_token, str):
        raise AppleTokenError("Missing id_token")

    try:
        header = jwt.get_unverified_header(id_token)
        kid = header.get("kid")
        alg = header.get("alg")
        if not kid or not alg:
            raise AppleTokenError("Invalid token header")
    except Exception as e:
        raise AppleTokenError(f"Invalid token header: {e}") from e

    jwks = _jwks_cache.get()
    keys = jwks.get("keys", [])
    key = next((k for k in keys if k.get("kid") == kid), None)
    if not key:
        raise AppleTokenError("Apple public key not found for token kid")

    try:
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
        claims = jwt.decode(
            id_token,
            key=public_key,
            algorithms=[alg],
            audience=audience,
            issuer=issuer,
            leeway=leeway_seconds,
            options={
                "require": ["exp", "iat", "iss", "aud", "sub"],
            },
        )
    except jwt.ExpiredSignatureError as e:
        raise AppleTokenError("Token expired") from e
    except jwt.InvalidAudienceError as e:
        raise AppleTokenError("Invalid audience") from e
    except jwt.InvalidIssuerError as e:
        raise AppleTokenError("Invalid issuer") from e
    except Exception as e:
        raise AppleTokenError(f"Token verification failed: {e}") from e

    email = claims.get("email")
    email_verified_raw = claims.get("email_verified")
    email_verified = None
    if isinstance(email_verified_raw, str):
        email_verified = email_verified_raw.lower() == "true"
    elif isinstance(email_verified_raw, bool):
        email_verified = email_verified_raw

    return AppleClaims(
        sub=str(claims.get("sub")),
        email=str(email) if email is not None else None,
        email_verified=email_verified,
        iss=str(claims.get("iss")),
        aud=str(claims.get("aud")),
        iat=int(claims.get("iat")),
        exp=int(claims.get("exp")),
    )