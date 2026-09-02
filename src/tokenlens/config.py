"""Environment-backed TokenLens settings."""

from __future__ import annotations

import math
import os
from dataclasses import dataclass
from pathlib import Path

from tokenlens.estimator import OutputMode
from tokenlens.models import get_model_rates


@dataclass(frozen=True, slots=True)
class Settings:
    default_model: str = "claude-sonnet"
    output_mode: OutputMode = OutputMode.BALANCED
    warning_budget_usd: float = 0.05
    history_path: Path = Path(".tokenlens/history.jsonl")


def load_settings(environment: dict[str, str] | None = None) -> Settings:
    values = os.environ if environment is None else environment
    model = values.get("TOKENLENS_MODEL", "claude-sonnet").strip()
    if not model:
        raise ValueError("TOKENLENS_MODEL must be non-empty")
    get_model_rates(model)
    try:
        output_mode = OutputMode(
            values.get("TOKENLENS_OUTPUT_MODE", OutputMode.BALANCED).strip()
        )
    except ValueError as exc:
        raise ValueError("TOKENLENS_OUTPUT_MODE is invalid") from exc
    raw_budget = values.get("TOKENLENS_WARNING_BUDGET_USD", "0.05").strip()
    try:
        budget = float(raw_budget)
    except ValueError as exc:
        raise ValueError("TOKENLENS_WARNING_BUDGET_USD must be a number") from exc
    if not math.isfinite(budget) or budget < 0:
        raise ValueError("TOKENLENS_WARNING_BUDGET_USD must be finite and non-negative")
    raw_history_path = values.get(
        "TOKENLENS_HISTORY_PATH", ".tokenlens/history.jsonl"
    ).strip()
    if not raw_history_path:
        raise ValueError("TOKENLENS_HISTORY_PATH must be non-empty")
    history_path = Path(raw_history_path)
    return Settings(
        default_model=model,
        output_mode=output_mode,
        warning_budget_usd=budget,
        history_path=history_path,
    )
