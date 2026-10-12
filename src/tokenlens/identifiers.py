"""Deterministic identifiers for repeatable analyses."""

from __future__ import annotations

import hashlib
import json

from tokenlens.contracts import EstimateRequest


def analysis_id_for(request: EstimateRequest) -> str:
    prompt_digest = hashlib.sha256(request.prompt.encode("utf-8")).hexdigest()
    identity = {
        "cached_context_tokens": request.cached_context_tokens,
        "context_tokens": request.context_tokens,
        "maximum_output_tokens": request.maximum_output_tokens,
        "model": request.model,
        "output_mode": request.output_mode.value,
        "prompt_digest": prompt_digest,
    }
    encoded = json.dumps(
        identity,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return f"tl_{hashlib.sha256(encoded).hexdigest()[:24]}"
