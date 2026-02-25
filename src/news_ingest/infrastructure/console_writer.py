from __future__ import annotations

import json

from news_ingest.application.ports import StreamWriterPort


class ConsoleWriter(StreamWriterPort):
    def put_record(self, *, data: dict[str, object], partition_key: str) -> None:
        _ = partition_key
        print(json.dumps(data, ensure_ascii=False))
