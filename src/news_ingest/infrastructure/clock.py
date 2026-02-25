from __future__ import annotations

from datetime import datetime, timezone

from news_ingest.application.ports import ClockPort


class UtcClock(ClockPort):
    def now(self) -> datetime:
        return datetime.now(timezone.utc)