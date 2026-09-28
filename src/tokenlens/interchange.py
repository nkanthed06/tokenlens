"""Portable estimate-history formats."""

from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict
from pathlib import Path

from tokenlens.history import EstimateRecord

_CSV_FIELDS = (
    "recorded_at",
    "model",
    "prompt_tokens",
    "context_tokens",
    "output_tokens",
    "total_cost",
)


def export_csv(records: list[EstimateRecord], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as export_file:
        writer = csv.DictWriter(export_file, fieldnames=_CSV_FIELDS)
        writer.writeheader()
        writer.writerows(asdict(record) for record in records)


def export_json(records: list[EstimateRecord], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps([asdict(record) for record in records], indent=2, sort_keys=True),
        encoding="utf-8",
    )


def import_json(path: Path) -> list[EstimateRecord]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("history import is not valid JSON") from exc
    if not isinstance(payload, list):
        raise ValueError("history import must contain an array")
    return [_parse_record(item, index) for index, item in enumerate(payload)]


def _parse_record(payload: object, index: int) -> EstimateRecord:
    if not isinstance(payload, dict) or set(payload) != set(_CSV_FIELDS):
        raise ValueError(f"history record {index} has invalid fields")
    for field in ("prompt_tokens", "context_tokens", "output_tokens"):
        value = payload[field]
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"history record {index} has invalid {field}")
    total_cost = payload["total_cost"]
    if (
        not isinstance(total_cost, (int, float))
        or isinstance(total_cost, bool)
        or not math.isfinite(total_cost)
        or total_cost < 0
    ):
        raise ValueError(f"history record {index} has invalid total_cost")
    for field in ("recorded_at", "model"):
        value = payload[field]
        if not isinstance(value, str) or not value:
            raise ValueError(f"history record {index} has invalid {field}")
    return EstimateRecord(
        recorded_at=payload["recorded_at"],
        model=payload["model"],
        prompt_tokens=payload["prompt_tokens"],
        context_tokens=payload["context_tokens"],
        output_tokens=payload["output_tokens"],
        total_cost=float(total_cost),
    )
