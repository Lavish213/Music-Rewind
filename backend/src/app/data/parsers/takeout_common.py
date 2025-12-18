# location: backend/src/app/data/parsers/takeout_common.py
# purpose: Shared types + helpers for Google Takeout parsing (HTML + JSON)

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
import hashlib
import json
import logging
import re

log = logging.getLogger(__name__)


# -------------------------
# Exceptions
# -------------------------
class TakeoutParseError(RuntimeError):
    pass


# -------------------------
# Core record shape
# -------------------------
@dataclass(frozen=True)
class TakeoutEvent:
    """
    A single normalized activity row/event extracted from Takeout.

    Think of this as the "raw gold" we pull out before mapping to DB models.
    """
    source_file: str
    source_kind: str  # "html" | "json"
    occurred_at: Optional[datetime]

    # Best-effort normalized fields
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None

    # Free-form payload (original row, keep for debugging)
    raw: Optional[Dict[str, Any]] = None

    # A stable fingerprint so we can dedupe
    fingerprint: Optional[str] = None


@dataclass(frozen=True)
class ParseReport:
    source_file: str
    count: int
    errors: List[str]


# -------------------------
# Small utilities
# -------------------------
_WS_RE = re.compile(r"\s+")
_TAG_RE = re.compile(r"<[^>]+>")
_YT_TIME_KEYS = ("time", "timestamp", "header", "eventTime")


def compact_ws(s: str) -> str:
    return _WS_RE.sub(" ", s).strip()


def strip_html_tags(s: str) -> str:
    # not a full HTML parser, but safe enough for takeout text blocks
    return compact_ws(_TAG_RE.sub(" ", s))


def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", errors="ignore")).hexdigest()


def safe_read_text(path: Path) -> str:
    # Google Takeout files are typically UTF-8, but sometimes have odd chars.
    # We keep it resilient.
    return path.read_text(encoding="utf-8", errors="replace")


def safe_load_json(path: Path) -> Any:
    txt = safe_read_text(path)
    try:
        return json.loads(txt)
    except Exception as e:
        raise TakeoutParseError(f"Invalid JSON in {path}: {e}") from e


def parse_iso_datetime(value: str) -> Optional[datetime]:
    """
    Accepts:
    - 2023-01-15T03:20:11.123Z
    - 2023-01-15T03:20:11Z
    - 2023-01-15T03:20:11+00:00
    """
    v = value.strip()
    if not v:
        return None

    # Normalize Z
    if v.endswith("Z"):
        v = v[:-1] + "+00:00"

    try:
        dt = datetime.fromisoformat(v)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def best_effort_datetime(obj: Dict[str, Any]) -> Optional[datetime]:
    """
    Attempts to locate a datetime field inside a Takeout JSON item.
    """
    for k in _YT_TIME_KEYS:
        val = obj.get(k)
        if isinstance(val, str):
            dt = parse_iso_datetime(val)
            if dt:
                return dt
    return None


def normalize_title_artist(title: Optional[str], artist: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    t = compact_ws(title) if title else None
    a = compact_ws(artist) if artist else None

    # Remove common junk prefixes
    if t:
        t = re.sub(r"^(Watched|Listened to|Viewed|Played)\s+", "", t, flags=re.IGNORECASE).strip()
        t = t.strip(" -–—")

    if a:
        a = a.strip(" -–—")

    return (t or None, a or None)


def make_fingerprint(
    occurred_at: Optional[datetime],
    title: Optional[str],
    artist: Optional[str],
    source_file: str,
) -> str:
    """
    Dedupe key: time + title + artist (+ file path as salt).
    """
    ts = occurred_at.isoformat() if occurred_at else ""
    base = f"{ts}|{title or ''}|{artist or ''}|{source_file}"
    return sha256_hex(base)


def iter_takeout_files(root: Path, suffixes: Tuple[str, ...] = (".json", ".html")) -> Iterable[Path]:
    if root.is_file():
        if root.suffix.lower() in suffixes:
            yield root
        return

    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in suffixes:
            yield p


def looks_like_takeout_music_title(s: str) -> bool:
    """
    Heuristic: used to decide if a title line is probably a track title.
    """
    if not s:
        return False
    bad = ("http://", "https://", "google", "youtube", "search", "visited", "used")
    low = s.lower()
    return not any(b in low for b in bad)


def build_event(
    *,
    source_file: Path,
    source_kind: str,
    occurred_at: Optional[datetime],
    title: Optional[str],
    artist: Optional[str],
    album: Optional[str] = None,
    raw: Optional[Dict[str, Any]] = None,
) -> TakeoutEvent:
    title, artist = normalize_title_artist(title, artist)
    fp = make_fingerprint(occurred_at, title, artist, str(source_file))
    return TakeoutEvent(
        source_file=str(source_file),
        source_kind=source_kind,
        occurred_at=occurred_at,
        title=title,
        artist=artist,
        album=album,
        raw=raw or None,
        fingerprint=fp,
    )