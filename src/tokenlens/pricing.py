"""Token-based cost calculations."""

from __future__ import annotations

from dataclasses import dataclass

from tokenlens.models import get_model_rates

_PER_MILLION = 1_000_000


@dataclass(frozen=True, slots=True)
class CostEstimate:
    model: str
    input_tokens: int
    output_tokens: int
    cached_input_tokens: int
    input_cost: float
    output_cost: float
    total_cost: float


def estimate_cost(
    model: str,
    *,
    input_tokens: int,
    output_tokens: int,
    cached_input_tokens: int = 0,
) -> CostEstimate:
    for name, value in (
        ("input_tokens", input_tokens),
        ("output_tokens", output_tokens),
        ("cached_input_tokens", cached_input_tokens),
    ):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"{name} must be a non-negative integer")

    rates = get_model_rates(model)
    cached_rate = rates.cached_input_per_million or rates.input_per_million
    input_cost = (
        input_tokens * rates.input_per_million
        + cached_input_tokens * cached_rate
    ) / _PER_MILLION
    output_cost = output_tokens * rates.output_per_million / _PER_MILLION
    return CostEstimate(
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cached_input_tokens=cached_input_tokens,
        input_cost=input_cost,
        output_cost=output_cost,
        total_cost=input_cost + output_cost,
    )
