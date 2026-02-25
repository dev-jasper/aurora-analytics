from __future__ import annotations

from datetime import datetime
from typing import Any, Protocol


class ClockPort(Protocol):
    def now(self) -> datetime: ...


class NewsSourcePort(Protocol):
    def fetch_articles(self) -> list[dict[str, Any]]: ...


class StreamWriterPort(Protocol):
    def put_record(self, *, data: dict[str, Any], partition_key: str) -> None: ...
