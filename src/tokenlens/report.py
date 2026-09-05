"""Human-readable estimate reports."""

from __future__ import annotations

from tokenlens.estimator import TurnEstimate


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
