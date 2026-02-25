# News Ingest Pipeline (NewsAPI -> Kinesis)

This project periodically fetches articles from NewsAPI (Everything API),
cleans + validates them into a consistent JSON payload, and publishes each
article to an AWS Kinesis Data Stream.

## Requirements covered
- Fetch from NewsAPI Everything API on an interval
- Clean/validate into JSON fields:
  - article_id
  - source_name
  - title
  - content
  - Url
  - author
  - published_at
  - ingested_at
- Publish to AWS Kinesis Data Stream
- Dockerfile + README included

## Setup

### Environment variables
Required:
- `NEWSAPI_API_KEY` - your NewsAPI key
- `KINESIS_STREAM_NAME` - Kinesis Data Stream name
- `AWS_REGION` - e.g. `ap-southeast-1`

Optional:
- `NEWSAPI_QUERY` (default: `market`)
- `NEWSAPI_LANGUAGE` (default: `en`)
- `NEWSAPI_PAGE_SIZE` (default: `50`)
- `POLL_INTERVAL_SECONDS` (default: `60`)

AWS credentials:
- Use any standard AWS auth method supported by boto3:
  - `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN` (optional)
  - or IAM role (recommended in real deployments)

### Run locally (venv)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -U pip
pip install -e ".[dev]"

python -m news_ingest.main