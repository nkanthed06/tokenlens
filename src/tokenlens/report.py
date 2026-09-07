"""Human-readable estimate reports."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from tokenlens.estimator import TurnEstimate


class RecommendationLevel(StrEnum):
    OK = "ok"
    REVIEW = "review"
    HIGH = "high"


@dataclass(frozen=True, slots=True)
class Recommendation:
    level: RecommendationLevel
    message: str


def render_summary(estimate: TurnEstimate) -> str:
    cached = estimate.cached_context_tokens
    uncached = estimate.context_tokens - cached
    rows = (
        ("Model", estimate.model),
        ("Prompt", f"~{estimate.prompt.estimated_tokens:,} tokens"),
        ("Context", f"{estimate.context_tokens:,} tokens"),
        ("Cached context", f"{cached:,} tokens"),
        ("Uncached context", f"{uncached:,} tokens"),
        ("Predicted output", f"~{estimate.output_tokens:,} tokens"),
        ("Estimated cost", f"${estimate.cost.total_cost:.6f}"),
    )
    width = max(len(label) for label, _ in rows)
    return "\n".join(f"{label.ljust(width)}  {value}" for label, value in rows)


def recommend(
    estimate: TurnEstimate,
    *,
    warning_budget_usd: float,
) -> Recommendation:
    if warning_budget_usd < 0:
        raise ValueError("warning_budget_usd must be non-negative")
    if estimate.cost.total_cost > warning_budget_usd:
        return Recommendation(
            RecommendationLevel.HIGH,
            "Estimated cost exceeds the configured warning budget.",
        )
    if estimate.context_tokens > max(4_000, estimate.prompt.estimated_tokens * 20):
        return Recommendation(
            RecommendationLevel.REVIEW,
            "Carried context dominates this turn; consider starting a focused session.",
        )
    if estimate.prompt.estimated_tokens > 2_000:
        return Recommendation(
            RecommendationLevel.REVIEW,
            "The prompt is large; remove repeated instructions or unrelated context.",
        )
    return Recommendation(
        RecommendationLevel.OK,
        "The estimate is within the configured review thresholds.",
    )
