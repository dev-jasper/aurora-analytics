Aurora Analytics — News Ingest Pipeline
  Overview

  Aurora Analytics is a Python-based data ingestion pipeline that fetches news articles from the NewsAPI “Everything” endpoint, normalizes the data into a consistent schema, and streams records through a pluggable output writer.


Architecture:
  The system follows a layered design:
  domain/
      models.py        → Business entities (NewsArticle)
  application/
      use_cases.py     → Core ingestion logic
      ports.py         → Interfaces (ClockPort, StreamWriterPort, NewsSourcePort)
  infrastructure/
      newsapi_client.py → External API adapter
      console_writer.py → Local output adapter
      kinesis_writer.py → AWS Kinesis adapter
      settings.py       → Environment configuration
  Flow
  NewsAPI → UseCase → Writer Adapter
  The use case is unaware of infrastructure details.
  Output behavior is swapped through dependency injection.

Features:
  Polls NewsAPI periodically
  Normalizes article payloads
  Generates deterministic article_id
  Streams records via adapter pattern
  Structured logging
  Docker-ready

Requirements:
  Python 3.11+
    pip
    NewsAPI account

    Optional (for cloud mode):
      AWS account
      Kinesis stream

  Environment Variables
  Required
  NEWSAPI_API_KEY=your_key_here

  Run Locally (Console Mode)

  Windows CMD:
    set NEWSAPI_API_KEY=YOUR_KEY
    python -m news_ingest.main


  Run with AWS Kinesis:
    Replace the writer inside main.py with KinesisWriter if desired.
    Set AWS variables:
      set NEWSAPI_API_KEY=YOUR_KEY
      set AWS_REGION=ap-southeast-1
      set KINESIS_STREAM_NAME=aurora-stream
      python -m news_ingest.main

  Docker:
    Build:
    docker build -t aurora-analytics .

    Linting & Style
      ruff check .

  Expected Result:
    Example record:
    {
      "article_id": "...",
      "source_name": "...",
      "title": "...",
      "content": "...",
      "Url": "...",
      "author": "...",
      "published_at": "...",
      "ingested_at": "..."
    }