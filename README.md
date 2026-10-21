# TokenLens

TokenLens is a local-first Python toolkit for estimating AI prompt tokens,
predicted output size, and request cost before a prompt is sent to a provider.
It includes a CLI, a reusable service boundary, privacy-safe history, and CSV or
JSON interchange helpers.

## Features

- Dependency-free local token approximation
- Versioned pricing for supported Claude and GPT model families
- Cached-context and output-mode cost estimates
- Strict model aliases with no silent pricing fallback
- Deterministic analysis IDs that do not contain prompt text
- Optional history containing derived metrics only
- Configurable cost warnings and operational input limits

## Requirements

- Python 3.11 or newer

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## CLI

Estimate a turn:

```bash
tokenlens estimate "Summarize this design document" \
  --model claude-sonnet \
  --context-tokens 12000 \
  --cached-context-tokens 8000
```

Return machine-readable output:

```bash
tokenlens estimate "Review this patch" --model gpt-4.1-mini --json
```

## Python API

```python
from tokenlens.service import analyze_request

result = analyze_request(
    {
        "prompt": "Explain the performance regression.",
        "model": "claude-sonnet-4",
        "context_tokens": 5000,
        "output_mode": "concise",
    }
)

print(result["analysis_id"])
print(result["estimate"]["cost"]["total_cost"])
print(result["recommendation"]["message"])
```

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `TOKENLENS_MODEL` | `claude-sonnet` | Default model |
| `TOKENLENS_OUTPUT_MODE` | `balanced` | Output estimate mode |
| `TOKENLENS_WARNING_BUDGET_USD` | `0.05` | Cost review threshold |
| `TOKENLENS_HISTORY_PATH` | `.tokenlens/history.jsonl` | Local history file |

Pricing is an estimate based on the catalog in `src/tokenlens/models.py`. Verify
provider pricing before using estimates for billing or purchasing decisions.

## Privacy

Token estimation runs locally. Saved history contains timestamps, model names,
derived token counts, and estimated cost; it does not store raw prompts.

## Development

```bash
uvx ruff check .
PYTHONPATH=src python3 -m unittest discover -s tests
python3 scripts/package_smoke.py
```

The full 12-week development history is documented in
[`docs/commit-backlog.md`](docs/commit-backlog.md).
