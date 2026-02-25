from __future__ import annotations

import logging
import time

from news_ingest.application.use_cases import IngestNewsUseCase
from news_ingest.infrastructure.clock import UtcClock
from news_ingest.infrastructure.console_writer import ConsoleWriter
from news_ingest.infrastructure.newsapi_client import NewsApiClient
from news_ingest.infrastructure.settings import Settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger("news_ingest")


def main() -> None:
    settings = Settings.from_env()

    # Composition root (lightweight DI)
    clock = UtcClock()
    news_source = NewsApiClient(settings=settings)
    stream_writer = ConsoleWriter()
    use_case = IngestNewsUseCase(
        news_source=news_source,
        stream_writer=stream_writer,
        clock=clock,
    )

    logger.info("Starting pipeline. Poll interval=%ss", settings.poll_interval_seconds)

    while True:
        counters = use_case.run_once()
        logger.info("Cycle complete: %s", counters)
        time.sleep(settings.poll_interval_seconds)


if __name__ == "__main__":
    main()
