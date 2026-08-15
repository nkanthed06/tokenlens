"""High-level turn estimation."""

from __future__ import annotations

from enum import StrEnum


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
