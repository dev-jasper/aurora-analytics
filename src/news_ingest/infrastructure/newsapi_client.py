from __future__ import annotations

from typing import Any

import requests

from news_ingest.application.ports import NewsSourcePort
from news_ingest.infrastructure.settings import Settings


class NewsApiClient(NewsSourcePort):
    BASE_URL = "https://newsapi.org/v2/everything"

    def __init__(self, *, settings: Settings, timeout_seconds: int = 15) -> None:
        self._settings = settings
        self._timeout_seconds = timeout_seconds

    def fetch_articles(self) -> list[dict[str, Any]]:
        headers = {"X-Api-Key": self._settings.newsapi_api_key}
        params = {
            "q": self._settings.newsapi_query,
            "language": self._settings.newsapi_language,
            "pageSize": self._settings.newsapi_page_size,
            "sortBy": "publishedAt",
        }

        resp = requests.get(
            self.BASE_URL,
            headers=headers,
            params=params,
            timeout=self._timeout_seconds,
        )
        resp.raise_for_status()

        data = resp.json()
        articles = data.get("articles")
        if not isinstance(articles, list):
            return []
        return [a for a in articles if isinstance(a, dict)]
