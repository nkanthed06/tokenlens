"""Operational limits for predictable local analysis."""

MAX_PROMPT_CHARACTERS = 1_000_000
MAX_CONTEXT_TOKENS = 2_000_000
MAX_OUTPUT_TOKENS = 200_000


def ensure_at_most(value: int, *, name: str, maximum: int) -> None:
    if value > maximum:
        raise ValueError(f"{name} cannot exceed {maximum:,}")


def ensure_prompt_within_limit(prompt: str) -> None:
    if len(prompt) > MAX_PROMPT_CHARACTERS:
        raise ValueError(
            f"prompt cannot exceed {MAX_PROMPT_CHARACTERS:,} characters"
        )
