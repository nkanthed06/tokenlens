"""Versioned model pricing catalog."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ModelRates:
    input_per_million: float
    output_per_million: float
    cached_input_per_million: float | None = None


MODEL_CATALOG: dict[str, ModelRates] = {
    "claude-haiku": ModelRates(1.0, 5.0, 0.1),
    "claude-sonnet": ModelRates(3.0, 15.0, 0.3),
    "claude-opus": ModelRates(15.0, 75.0, 1.5),
    "gpt-4.1-mini": ModelRates(0.4, 1.6, 0.1),
    "gpt-4.1": ModelRates(2.0, 8.0, 0.5),
}


def available_models() -> tuple[str, ...]:
    return tuple(sorted(MODEL_CATALOG))


def get_model_rates(model: str) -> ModelRates:
    try:
        return MODEL_CATALOG[model]
    except KeyError as exc:
        raise ValueError(f"unsupported model: {model}") from exc
