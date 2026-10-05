"""Versioned model pricing catalog."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ModelRates:
    input_per_million: float
    output_per_million: float
    cached_input_per_million: float | None = None


class UnsupportedModelError(ValueError):
    """Raised when TokenLens has no explicit pricing entry for a model."""


MODEL_CATALOG: dict[str, ModelRates] = {
    "claude-haiku": ModelRates(1.0, 5.0, 0.1),
    "claude-sonnet": ModelRates(3.0, 15.0, 0.3),
    "claude-opus": ModelRates(15.0, 75.0, 1.5),
    "gpt-4.1-mini": ModelRates(0.4, 1.6, 0.1),
    "gpt-4.1": ModelRates(2.0, 8.0, 0.5),
}

MODEL_ALIASES: dict[str, str] = {
    "claude-3-5-haiku-latest": "claude-haiku",
    "claude-sonnet-4": "claude-sonnet",
    "claude-opus-4": "claude-opus",
    "gpt-4.1-mini-2025-04-14": "gpt-4.1-mini",
}


def available_models() -> tuple[str, ...]:
    return tuple(sorted(MODEL_CATALOG))


def resolve_model(model: str) -> str:
    if not isinstance(model, str) or not model.strip():
        raise ValueError("model must be a non-empty string")
    normalized = model.strip().casefold()
    if normalized in MODEL_CATALOG:
        return normalized
    if normalized in MODEL_ALIASES:
        return MODEL_ALIASES[normalized]
    supported = ", ".join(available_models())
    raise UnsupportedModelError(
        f"unsupported model: {model}. Supported models: {supported}"
    )


def get_model_rates(model: str) -> ModelRates:
    resolved = resolve_model(model)
    return MODEL_CATALOG[resolved]
