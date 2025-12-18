# LOCATION: backend/src/app/integrations/google_oauth/scopes.py
# COMMENT: Central place for Google OAuth scopes used by the app

from __future__ import annotations

YT_READONLY = "https://www.googleapis.com/auth/youtube.readonly"
YT_WRITE = "https://www.googleapis.com/auth/youtube"

# Common identity scopes (optional, but typical)
OPENID = "openid"
EMAIL = "email"
PROFILE = "profile"

DEFAULT_SCOPES: list[str] = [
    OPENID,
    EMAIL,
    PROFILE,
    YT_READONLY,
]