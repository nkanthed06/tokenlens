"""High-level turn estimation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from tokenlens.pricing import CostEstimate, estimate_cost
from tokenlens.tokenizer import TokenCount, analyze_text


class OutputMode(StrEnum):
    CONCISE = "concise"
    BALANCED = "balanced"
    DETAILED = "detailed"


_OUTPUT_RATIOS = {
    OutputMode.CONCISE: 0.35,
    OutputMode.BALANCED: 0.75,
    OutputMode.DETAILED: 1.5,
}
_MINIMUM_OUTPUT_TOKENS = 64


@dataclass(frozen=True, slots=True)
class TurnEstimate:
    model: str
    prompt: TokenCount
    context_tokens: int
    cached_context_tokens: int
    output_tokens: int
    cost: CostEstimate


def estimate_output_tokens(
    prompt_tokens: int,
    *,
    mode: OutputMode | str = OutputMode.BALANCED,
    maximum: int | None = None,
) -> int:
    if not isinstance(prompt_tokens, int) or isinstance(prompt_tokens, bool):
        raise ValueError("prompt_tokens must be an integer")
    if prompt_tokens < 0:
        raise ValueError("prompt_tokens must be non-negative")
    try:
        resolved_mode = OutputMode(mode)
    except ValueError as exc:
        raise ValueError(f"unsupported output mode: {mode}") from exc
    estimate = max(_MINIMUM_OUTPUT_TOKENS, round(prompt_tokens * _OUTPUT_RATIOS[resolved_mode]))
    if maximum is None:
        return estimate
    if not isinstance(maximum, int) or isinstance(maximum, bool) or maximum <= 0:
        raise ValueError("maximum must be a positive integer")
    return min(estimate, maximum)


def estimate_turn(
    prompt: str,
    *,
    model: str,
    context_tokens: int = 0,
    cached_context_tokens: int = 0,
    output_mode: OutputMode | str = OutputMode.BALANCED,
    maximum_output_tokens: int | None = None,
) -> TurnEstimate:
    for name, value in (
        ("context_tokens", context_tokens),
        ("cached_context_tokens", cached_context_tokens),
    ):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"{name} must be a non-negative integer")
    if cached_context_tokens > context_tokens:
        raise ValueError("cached_context_tokens cannot exceed context_tokens")

    prompt_count = analyze_text(prompt)
    output_tokens = estimate_output_tokens(
        prompt_count.estimated_tokens,
        mode=output_mode,
        maximum=maximum_output_tokens,
    )
    uncached_context = context_tokens - cached_context_tokens
    cost = estimate_cost(
        model,
        input_tokens=prompt_count.estimated_tokens + uncached_context,
        cached_input_tokens=cached_context_tokens,
        output_tokens=output_tokens,
    )
    return TurnEstimate(
        model=model,
        prompt=prompt_count,
        context_tokens=context_tokens,
        cached_context_tokens=cached_context_tokens,
        output_tokens=output_tokens,
        cost=cost,
    )
