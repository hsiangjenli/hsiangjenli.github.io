"""Client for the blog's small static posts API."""

from datetime import datetime, timezone
from typing import Any

import requests


def latest_posts(api_url: str, locale: str, limit: int = 10) -> list[dict[str, Any]]:
    """Return recent posts for one locale; an unavailable API yields no posts."""
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError):
        return []
    posts = payload.get("posts", [])
    if not isinstance(posts, list):
        return []
    selected = [
        post for post in posts
        if isinstance(post, dict) and post.get("lang", "en") == locale
        and "[chatgpt]" not in str(post.get("title", "")).lower()
    ]
    return sorted(selected, key=_post_date, reverse=True)[:limit]


def _post_date(post: dict[str, Any]) -> datetime:
    value = str(post.get("updated") or post.get("date") or "")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)
