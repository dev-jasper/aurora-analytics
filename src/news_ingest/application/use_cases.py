from __future__ import annotations

import logging

from news_ingest.application.ports import ClockPort, NewsSourcePort, StreamWriterPort
from news_ingest.domain.models import NewsArticle

logger = logging.getLogger(__name__)


class IngestNewsUseCase:
    def __init__(
        self,
        *,
        news_source: NewsSourcePort,
        stream_writer: StreamWriterPort,
        clock: ClockPort,
    ) -> None:
        self._news_source = news_source
        self._stream_writer = stream_writer
        self._clock = clock

    def run_once(self) -> dict[str, int]:
        fetched = 0
        ingested = 0
        failed = 0

        articles = self._news_source.fetch_articles()
        fetched = len(articles)
        ingested_at = self._clock.now()

        for raw in articles:
            try:
                article = NewsArticle.from_newsapi(raw, ingested_at=ingested_at)
                self._stream_writer.put_record(
                    data=article.to_dict(),
                    partition_key=article.article_id,
                )
                ingested += 1
            except Exception:
                failed += 1
                logger.exception("Failed to process article")

        return {"fetched": fetched, "ingested": ingested, "failed": failed}
