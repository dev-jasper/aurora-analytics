from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any


def parse_iso8601(value: str) -> datetime:
    v = value.strip()
    if v.endswith("Z"):
        v = v[:-1] + "+00:00"
    dt = datetime.fromisoformat(v)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def compute_article_id(url: str, published_at: datetime, title: str) -> str:
    raw = f"{url}|{published_at.isoformat()}|{title}".encode("utf-8")
    return sha256(raw).hexdigest()


@dataclass(frozen=True)
class NewsArticle:
    article_id: str
    source_name: str
    title: str
    content: str
    Url: str  # requirement field name uses capital U
    author: str
    published_at: datetime
    ingested_at: datetime

    def to_dict(self) -> dict[str, Any]:
        return {
            "article_id": self.article_id,
            "source_name": self.source_name,
            "title": self.title,
            "content": self.content,
            "Url": self.Url,
            "author": self.author,
            "published_at": self.published_at.isoformat(),
            "ingested_at": self.ingested_at.isoformat(),
        }

    @staticmethod
    def from_newsapi(
        payload: dict[str, Any],
        *,
        ingested_at: datetime,
    ) -> "NewsArticle":
        source = payload.get("source") or {}
        source_name = str(source.get("name") or "").strip()

        title = str(payload.get("title") or "").strip()
        content = str(payload.get("content") or "").strip()

        url = str(payload.get("url") or "").strip()
        author = str(payload.get("author") or "").strip()

        published_raw = str(payload.get("publishedAt") or "").strip()
        if not published_raw:
            raise ValueError("publishedAt is required")
        published_at = parse_iso8601(published_raw)

        if not url:
            raise ValueError("url is required")

        article_id = compute_article_id(url, published_at, title)

        return NewsArticle(
            article_id=article_id,
            source_name=source_name,
            title=title,
            content=content,
            Url=url,
            author=author,
            published_at=published_at,
            ingested_at=ingested_at,
        )