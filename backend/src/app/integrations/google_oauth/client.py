# LOCATION: backend/src/app/integrations/google_oauth/client.py
# COMMENT: Exchange code for tokens + refresh tokens + minimal userinfo helpers

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional
from urllib.parse import urlencode

import requests


class GoogleOAuthError(Exception):
    pass


@dataclass(frozen=True)
class GoogleTokenResponse:
    access_token: str
    expires_in: int
    token_type: str
    refresh_token: Optional[str]
    scope: Optional[str]
    id_token: Optional[str]


GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


def exchange_code_for_tokens(
    *,
    code: str,
    client_id: str,
    client_secret: str,
    redirect_uri: str,
    timeout_sec: int = 15,
) -> GoogleTokenResponse:
    if not code:
        raise GoogleOAuthError("Missing code")

    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    try:
        r = requests.post(GOOGLE_TOKEN_URL, data=data, timeout=timeout_sec)
        payload: dict[str, Any] = r.json()
    except Exception as e:
        raise GoogleOAuthError(f"Token exchange failed: {e}") from e

    if r.status_code >= 400:
        raise GoogleOAuthError(f"Token exchange error: {payload}")

    access_token = payload.get("access_token")
    if not access_token:
        raise GoogleOAuthError(f"Missing access_token: {payload}")

    return GoogleTokenResponse(
        access_token=str(access_token),
        expires_in=int(payload.get("expires_in", 0)),
        token_type=str(payload.get("token_type", "Bearer")),
        refresh_token=payload.get("refresh_token"),
        scope=payload.get("scope"),
        id_token=payload.get("id_token"),
    )


def refresh_access_token(
    *,
    refresh_token: str,
    client_id: str,
    client_secret: str,
    timeout_sec: int = 15,
) -> GoogleTokenResponse:
    if not refresh_token:
        raise GoogleOAuthError("Missing refresh_token")

    data = {
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
    }

    try:
        r = requests.post(GOOGLE_TOKEN_URL, data=data, timeout=timeout_sec)
        payload: dict[str, Any] = r.json()
    except Exception as e:
        raise GoogleOAuthError(f"Token refresh failed: {e}") from e

    if r.status_code >= 400:
        raise GoogleOAuthError(f"Token refresh error: {payload}")

    access_token = payload.get("access_token")
    if not access_token:
        raise GoogleOAuthError(f"Missing access_token: {payload}")

    # Note: Google often does NOT return refresh_token again on refresh.
    return GoogleTokenResponse(
        access_token=str(access_token),
        expires_in=int(payload.get("expires_in", 0)),
        token_type=str(payload.get("token_type", "Bearer")),
        refresh_token=None,
        scope=payload.get("scope"),
        id_token=payload.get("id_token"),
    )


def get_userinfo(
    *,
    access_token: str,
    timeout_sec: int = 15,
) -> dict[str, Any]:
    if not access_token:
        raise GoogleOAuthError("Missing access_token")

    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        r = requests.get(GOOGLE_USERINFO_URL, headers=headers, timeout=timeout_sec)
        payload: dict[str, Any] = r.json()
    except Exception as e:
        raise GoogleOAuthError(f"Userinfo request failed: {e}") from e

    if r.status_code >= 400:
        raise GoogleOAuthError(f"Userinfo error: {payload}")

    return payload


def build_google_auth_url(
    *,
    client_id: str,
    redirect_uri: str,
    scopes: list[str],
    state: str,
    include_granted_scopes: bool = True,
    access_type: str = "offline",
    prompt: str = "consent",
) -> str:
    """
    Builds Google's OAuth consent screen URL (for your frontend or backend redirect).
    """
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(scopes),
        "state": state,
        "access_type": access_type,
        "prompt": prompt,
        "include_granted_scopes": "true" if include_granted_scopes else "false",
    }
    return "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)