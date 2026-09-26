"""Portable estimate-history formats."""

from __future__ import annotations

import csv
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
