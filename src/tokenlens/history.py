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
