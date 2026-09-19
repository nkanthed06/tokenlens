"""Validated service request contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from tokenlens.estimator import OutputMode
from tokenlens.models import get_model_rates


@dataclass(frozen=True, slots=True)
class EstimateRequest:
    prompt: str
    model: str
    context_tokens: int = 0
    cached_context_tokens: int = 0
    output_mode: OutputMode = OutputMode.BALANCED
    maximum_output_tokens: int | None = None


def parse_estimate_request(payload: object) -> EstimateRequest:
    if not isinstance(payload, dict):
        raise ValueError("request must be an object")
    prompt = payload.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("prompt must be a non-empty string")
    model = payload.get("model", "claude-sonnet")
    if not isinstance(model, str):
        raise ValueError("model must be a string")
    get_model_rates(model)
    context_tokens = _non_negative_integer(payload, "context_tokens", default=0)
    cached_context_tokens = _non_negative_integer(
        payload, "cached_context_tokens", default=0
    )
    if cached_context_tokens > context_tokens:
        raise ValueError("cached_context_tokens cannot exceed context_tokens")
    raw_mode = payload.get("output_mode", OutputMode.BALANCED)
    try:
        output_mode = OutputMode(raw_mode)
    except (TypeError, ValueError) as exc:
        raise ValueError("output_mode is invalid") from exc
    maximum = payload.get("maximum_output_tokens")
    if maximum is not None:
        maximum = _positive_integer(maximum, "maximum_output_tokens")
    return EstimateRequest(
        prompt=prompt,
        model=model,
        context_tokens=context_tokens,
        cached_context_tokens=cached_context_tokens,
        output_mode=output_mode,
        maximum_output_tokens=maximum,
    )


def _non_negative_integer(
    payload: dict[str, Any], name: str, *, default: int
) -> int:
    value = payload.get(name, default)
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")
    return value


def _positive_integer(value: object, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value
