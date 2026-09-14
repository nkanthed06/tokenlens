"""Append-only local history for derived estimate metrics."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from tokenlens.estimator import TurnEstimate


@dataclass(frozen=True, slots=True)
class EstimateRecord:
    recorded_at: str
    model: str
    prompt_tokens: int
    context_tokens: int
    output_tokens: int
    total_cost: float


@dataclass(frozen=True, slots=True)
class HistorySummary:
    estimates: int
    total_tokens: int
    total_cost: float
    average_cost: float


def record_from_estimate(
    estimate: TurnEstimate,
    *,
    recorded_at: datetime | None = None,
) -> EstimateRecord:
    timestamp = recorded_at or datetime.now(UTC)
    return EstimateRecord(
        recorded_at=timestamp.astimezone(UTC).isoformat(),
        model=estimate.model,
        prompt_tokens=estimate.prompt.estimated_tokens,
        context_tokens=estimate.context_tokens,
        output_tokens=estimate.output_tokens,
        total_cost=estimate.cost.total_cost,
    )


def append_record(path: Path, record: EstimateRecord) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as history_file:
        history_file.write(json.dumps(asdict(record), sort_keys=True))
        history_file.write("\n")


def read_records(path: Path) -> list[EstimateRecord]:
    if not path.exists():
        return []
    records = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
            records.append(EstimateRecord(**payload))
        except (json.JSONDecodeError, TypeError) as exc:
            raise ValueError(f"invalid history record on line {line_number}") from exc
    return records


def summarize_history(records: list[EstimateRecord]) -> HistorySummary:
    total_cost = sum(record.total_cost for record in records)
    total_tokens = sum(
        record.prompt_tokens + record.context_tokens + record.output_tokens
        for record in records
    )
    return HistorySummary(
        estimates=len(records),
        total_tokens=total_tokens,
        total_cost=total_cost,
        average_cost=total_cost / len(records) if records else 0.0,
    )
