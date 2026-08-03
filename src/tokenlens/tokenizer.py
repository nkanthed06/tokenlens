"""Dependency-free token approximations for fast local estimates."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass

_WORD_PATTERN = re.compile(r"\w+|[^\w\s]", re.UNICODE)


@dataclass(frozen=True, slots=True)
class TokenCount:
    characters: int
    words: int
    estimated_tokens: int


def estimate_tokens(text: str) -> int:
    """Estimate token usage without sending text to a remote tokenizer."""

    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not text:
        return 0
    lexical_units = len(_WORD_PATTERN.findall(text))
    character_floor = math.ceil(len(text) / 4)
    return max(1, lexical_units, character_floor)


def analyze_text(text: str) -> TokenCount:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return TokenCount(
        characters=len(text),
        words=len(text.split()),
        estimated_tokens=estimate_tokens(text),
    )
