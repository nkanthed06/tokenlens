"""TokenLens command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from dataclasses import asdict
from typing import TextIO

from tokenlens.estimator import OutputMode, estimate_turn
from tokenlens.models import available_models


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tokenlens")
    subparsers = parser.add_subparsers(dest="command", required=True)
    estimate = subparsers.add_parser("estimate", help="estimate one AI turn")
    estimate.add_argument("prompt")
    estimate.add_argument(
        "--model",
        choices=available_models(),
        default="claude-sonnet",
    )
    estimate.add_argument("--context-tokens", type=int, default=0)
    estimate.add_argument("--cached-context-tokens", type=int, default=0)
    estimate.add_argument("--json", action="store_true", dest="as_json")
    estimate.add_argument(
        "--output-mode",
        choices=tuple(OutputMode),
        default=OutputMode.BALANCED,
    )
    return parser


def _estimate(arguments: argparse.Namespace):
    return estimate_turn(
        arguments.prompt,
        model=arguments.model,
        context_tokens=arguments.context_tokens,
        cached_context_tokens=arguments.cached_context_tokens,
        output_mode=arguments.output_mode,
    )


def _render_estimate(arguments: argparse.Namespace) -> str:
    result = _estimate(arguments)
    return "\n".join(
        (
            f"Model: {result.model}",
            f"Prompt tokens: ~{result.prompt.estimated_tokens:,}",
            f"Context tokens: {result.context_tokens:,}",
            f"Predicted output: ~{result.output_tokens:,}",
            f"Estimated cost: ${result.cost.total_cost:.6f}",
        )
    )


def main(
    argv: Sequence[str] | None = None,
    *,
    stdout: TextIO | None = None,
) -> int:
    arguments = build_parser().parse_args(argv)
    destination = stdout or sys.stdout
    if arguments.command == "estimate":
        if arguments.as_json:
            rendered = json.dumps(asdict(_estimate(arguments)), sort_keys=True)
            print(rendered, file=destination)
        else:
            print(_render_estimate(arguments), file=destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
