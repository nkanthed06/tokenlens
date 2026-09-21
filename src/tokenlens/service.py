"""Reusable TokenLens analysis boundary."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from tokenlens.config import Settings, load_settings
from tokenlens.contracts import parse_estimate_request
from tokenlens.estimator import estimate_turn
from tokenlens.history import append_record, record_from_estimate
from tokenlens.report import recommend


def analyze_request(
    payload: object,
    *,
    settings: Settings | None = None,
    save_history: bool = False,
) -> dict[str, Any]:
    resolved_settings = settings or load_settings()
    normalized = dict(payload) if isinstance(payload, dict) else payload
    if isinstance(normalized, dict):
        normalized.setdefault("model", resolved_settings.default_model)
        normalized.setdefault("output_mode", resolved_settings.output_mode)
    request = parse_estimate_request(normalized)
    estimate = estimate_turn(
        request.prompt,
        model=request.model,
        context_tokens=request.context_tokens,
        cached_context_tokens=request.cached_context_tokens,
        output_mode=request.output_mode,
        maximum_output_tokens=request.maximum_output_tokens,
    )
    recommendation = recommend(
        estimate,
        warning_budget_usd=resolved_settings.warning_budget_usd,
    )
    if save_history:
        append_record(
            resolved_settings.history_path,
            record_from_estimate(estimate),
        )
    return {
        "estimate": asdict(estimate),
        "recommendation": asdict(recommendation),
    }
