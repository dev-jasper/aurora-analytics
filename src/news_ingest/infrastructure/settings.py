from __future__ import annotations

import os
from dataclasses import dataclass


def _req(name: str) -> str:
    v = os.getenv(name, "").strip()
    if not v:
        raise ValueError(f"Missing required environment variable: {name}")
    return v


def _opt_int(name: str, default: int) -> int:
    raw = os.getenv(name, "").strip()
    return default if not raw else int(raw)


@dataclass(frozen=True)
class Settings:
    newsapi_api_key: str
    newsapi_query: str
    newsapi_language: str
    newsapi_page_size: int
    poll_interval_seconds: int
    aws_region: str
    kinesis_stream_name: str

    @staticmethod
    def from_env() -> "Settings":
        return Settings(
            newsapi_api_key=_req("NEWSAPI_API_KEY"),
            newsapi_query=os.getenv("NEWSAPI_QUERY", "market"),
            newsapi_language=os.getenv("NEWSAPI_LANGUAGE", "en"),
            newsapi_page_size=_opt_int("NEWSAPI_PAGE_SIZE", 50),
            poll_interval_seconds=_opt_int("POLL_INTERVAL_SECONDS", 60),
            aws_region=_req("AWS_REGION"),
            kinesis_stream_name=_req("KINESIS_STREAM_NAME"),
        )