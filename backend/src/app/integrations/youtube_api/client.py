# LOCATION: backend/src/app/integrations/youtube_api/client.py
from __future__ import annotations

import json
import urllib.parse
import urllib.request
import urllib.error
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"


class YouTubeAPIError(RuntimeError):
    def __init__(self, status: int, message: str, payload: Optional[dict] = None):
        super().__init__(f"YouTube API error {status}: {message}")
        self.status = status
        self.payload = payload or {}


@dataclass(frozen=True)
class Page:
    items: List[Dict[str, Any]]
    next_page_token: Optional[str]


class YouTubeClient:
    """
    Minimal YouTube Data API v3 client using stdlib only.

    You provide an OAuth2 access token (Bearer) that has YouTube scopes.
    """

    def __init__(self, access_token: str, *, timeout_sec: int = 30):
        self._access_token = access_token
        self._timeout_sec = timeout_sec

    # -----------------------------
    # Core HTTP helpers
    # -----------------------------
    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{YOUTUBE_API_BASE}{path}"

        if params:
            cleaned = {k: v for k, v in params.items() if v is not None}
            url = f"{url}?{urllib.parse.urlencode(cleaned, doseq=True)}"

        data = None
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/json",
        }

        if body is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(body).encode("utf-8")

        req = urllib.request.Request(url, data=data, method=method, headers=headers)

        try:
            with urllib.request.urlopen(req, timeout=self._timeout_sec) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}

        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8") if hasattr(e, "read") else ""
            try:
                payload = json.loads(raw) if raw else {}
            except Exception:
                payload = {"raw": raw}

            message = payload.get("error", {}).get("message") or raw or str(e)
            raise YouTubeAPIError(e.code, message, payload)

        except urllib.error.URLError as e:
            raise RuntimeError(f"YouTube API network error: {e}") from e

    # -----------------------------
    # API methods
    # -----------------------------
    def channels_me(self) -> Dict[str, Any]:
        return self._request(
            "GET",
            "/channels",
            params={"part": "snippet,contentDetails,statistics", "mine": "true"},
        )

    def playlists_page(
        self,
        *,
        page_token: Optional[str] = None,
        max_results: int = 50,
    ) -> Page:
        data = self._request(
            "GET",
            "/playlists",
            params={
                "part": "snippet,contentDetails",
                "mine": "true",
                "maxResults": max(1, min(max_results, 50)),
                "pageToken": page_token,
            },
        )
        return Page(
            items=list(data.get("items", [])),
            next_page_token=data.get("nextPageToken"),
        )

    def playlist_items_page(
        self,
        playlist_id: str,
        *,
        page_token: Optional[str] = None,
        max_results: int = 50,
    ) -> Page:
        data = self._request(
            "GET",
            "/playlistItems",
            params={
                "part": "snippet,contentDetails",
                "playlistId": playlist_id,
                "maxResults": max(1, min(max_results, 50)),
                "pageToken": page_token,
            },
        )
        return Page(
            items=list(data.get("items", [])),
            next_page_token=data.get("nextPageToken"),
        )

    def videos_by_ids(self, video_ids: List[str]) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        for chunk in _chunks(video_ids, 50):
            data = self._request(
                "GET",
                "/videos",
                params={
                    "part": "snippet,contentDetails,statistics",
                    "id": ",".join(chunk),
                },
            )
            out.extend(list(data.get("items", [])))
        return out

    def iter_all_playlists(self) -> Iterable[Dict[str, Any]]:
        token = None
        while True:
            page = self.playlists_page(page_token=token)
            yield from page.items
            token = page.next_page_token
            if not token:
                break

    def iter_all_playlist_items(self, playlist_id: str) -> Iterable[Dict[str, Any]]:
        token = None
        while True:
            page = self.playlist_items_page(playlist_id, page_token=token)
            yield from page.items
            token = page.next_page_token
            if not token:
                break


def _chunks(items: List[str], n: int) -> Iterable[List[str]]:
    for i in range(0, len(items), n):
        yield items[i : i + n]


__all__ = ["YouTubeClient", "YouTubeAPIError"]