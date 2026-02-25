from __future__ import annotations

import json

import boto3

from news_ingest.application.ports import StreamWriterPort
from news_ingest.infrastructure.settings import Settings


class KinesisWriter(StreamWriterPort):
    def __init__(self, *, settings: Settings) -> None:
        self._stream_name = settings.kinesis_stream_name
        self._client = boto3.client("kinesis", region_name=settings.aws_region)

    def put_record(self, *, data: dict[str, object], partition_key: str) -> None:
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self._client.put_record(
            StreamName=self._stream_name,
            Data=payload,
            PartitionKey=partition_key,
        )
